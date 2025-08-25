from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional
from jose import jwt, JWTError
from ..config import settings

def _exp(minutes: int = 15) -> datetime:
    return datetime.now(timezone.utc) + timedelta(minutes=minutes)

def _exp_days(days: int = 30) -> datetime:
    return datetime.now(timezone.utc) + timedelta(days=days)

def create_access_token(data: Dict[str, Any]) -> str:
    payload = data.copy()
    payload.update({"type": "access", "exp": _exp(settings.access_token_minutes)})
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)

def create_refresh_token(data: Dict[str, Any]) -> str:
    payload = data.copy()
    payload.update({"type": "refresh", "exp": _exp_days(settings.refresh_token_days)})
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)

def verify_token(token: str, token_type: str = "access") -> Optional[Dict[str, Any]]:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        if payload.get("type") != token_type:
            return None
        return payload
    except JWTError:
        return None
