import uuid
from datetime import datetime, timezone, timedelta
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import User, RefreshToken
from ..utils.security import verify_password
from ..utils.jwt_utils import create_access_token, create_refresh_token

ACCESS_EXPIRES_SECONDS = 60 * 15  # 15 min

async def authenticate_user(db: AsyncSession, email: str, password: str) -> User | None:
    res = await db.execute(select(User).where(User.email == email))
    user = res.scalar_one_or_none()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

async def generate_tokens_for_user(db: AsyncSession, user: User) -> tuple[str, str, int]:
    payload = {"sub": str(user.id), "email": user.email, "role": user.role}
    access_token = create_access_token(payload)
    refresh_token = create_refresh_token(payload)

    # Store refresh token
    rt = RefreshToken(
        user_id=user.id,
        token=refresh_token,
        expires_at=datetime.now(timezone.utc) + timedelta(days=30),
        is_revoked=False,
    )
    db.add(rt)
    await db.commit()
    return access_token, refresh_token, ACCESS_EXPIRES_SECONDS

async def rotate_refresh_token(db: AsyncSession, token: str) -> tuple[str, str, int] | None:
    # Validate existing token
    res = await db.execute(select(RefreshToken).where(RefreshToken.token == token, RefreshToken.is_revoked == False))  # noqa: E712
    current = res.scalar_one_or_none()
    if not current:
        return None
    # Basic expiry check
    if current.expires_at < datetime.now(timezone.utc):
        return None

    # Load user
    user_res = await db.execute(select(User).where(User.id == current.user_id))
    user = user_res.scalar_one_or_none()
    if not user:
        return None

    # Revoke old token
    await db.execute(update(RefreshToken).where(RefreshToken.id == current.id).values(is_revoked=True))

    # Issue new pair
    return await generate_tokens_for_user(db, user)

async def revoke_refresh_token(db: AsyncSession, token: str) -> bool:
    res = await db.execute(select(RefreshToken).where(RefreshToken.token == token, RefreshToken.is_revoked == False))  # noqa: E712
    rt = res.scalar_one_or_none()
    if not rt:
        return False
    await db.execute(update(RefreshToken).where(RefreshToken.id == rt.id).values(is_revoked=True))
    await db.commit()
    return True
