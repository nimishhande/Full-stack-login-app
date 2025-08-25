# backend/app/routers/auth.py
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from ..config import settings
from ..services.oauth_service import oauth

router = APIRouter(prefix="/api/auth", tags=["auth"])

# Type hint for Pylance to know oauth.google exists
google_oauth: OAuth = oauth  # Pylance-friendly

@router.get("/google")
async def login_via_google(request: Request):
    """
    Redirects user to Google's OAuth login page.
    """
    redirect_uri = f"{settings.frontend_url}/auth/callback"
    # Use type ignore if Pylance still complains
    return await google_oauth.google.authorize_redirect(request, redirect_uri)  # type: ignore

@router.get("/google/callback")
async def auth_google_callback(request: Request):
    """
    Handles Google OAuth callback and returns user info.
    """
    try:
        token = await google_oauth.google.authorize_access_token(request)  # type: ignore
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"OAuth callback failed: {e}")

    user_info = token.get("userinfo")
    if not user_info:
        raise HTTPException(status_code=400, detail="Failed to fetch user info from Google")

    # Here you would create/find user in DB
    # For now, just return token and user info
    return {
        "access_token": token["access_token"],
        "user": user_info
    }
