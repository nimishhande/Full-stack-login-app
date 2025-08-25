from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import User
from ..utils.security import hash_password

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    res = await db.execute(select(User).where(User.email == email))
    return res.scalar_one_or_none()

async def create_user(db: AsyncSession, name: str, email: str, password: str | None, provider: str = "email", provider_id: str | None = None) -> User:
    user = User(
        name=name,
        email=email,
        password_hash=hash_password(password) if password else None,
        provider=provider,
        provider_id=provider_id,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
