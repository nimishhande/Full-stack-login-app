from fastapi import APIRouter, Depends
from ..middleware.auth_middleware import require_auth, require_role

router = APIRouter()

@router.get("/me")
async def me(claims: dict = Depends(require_auth)):
    return {"message": "ok", "claims": claims}

@router.get("/admin")
async def admin_only(_: dict = Depends(require_role("admin"))):
    return {"message": "admin ok"}
