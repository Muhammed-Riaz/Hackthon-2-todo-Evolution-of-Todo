"""
Authentication API routes for the backend application.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import Form
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from backend.src.database.database import get_async_session
from backend.src.models.user_model import User
from backend.src.schemas.auth_schemas import UserCreate, UserResponse, TokenResponse
from backend.src.services.user_service import create_user, authenticate_user
from backend.src.auth.jwt import create_access_token
from backend.src.core.config import get_settings
from backend.src.auth.dependencies import get_current_user_id

router = APIRouter(prefix="/api/auth", tags=["auth"])

settings = get_settings()

@router.post("/signup", response_model=TokenResponse)
async def signup_user(
    user_create: UserCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Register a new user and return an access token.
    """
    # Create the user using the service
    user = await create_user(session, user_create)

    # Create access token
    access_token = create_access_token(data={"sub": str(user.id)})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


class LoginRequest(BaseModel):
    """
    Request model for login endpoint to avoid FastAPI compatibility issues
    """
    username: str
    password: str


@router.post("/login", response_model=TokenResponse)
async def login_user(
    request: LoginRequest,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Login a user and return an access token.
    """
    user = await authenticate_user(
        session,
        request.username,  # email/username parameter
        request.password  # password parameter
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token = create_access_token(data={"sub": str(user.id)})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@router.post("/logout")
async def logout_user():
    """
    Logout the current user.
    """
    # In a stateless JWT system, the server doesn't maintain session state
    # The client should remove the token from storage
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user_id: str = Depends(get_current_user_id)):
    """
    Get current user information.
    """
    # This would normally fetch the user from the database using current_user_id
    # For now, we just return the user_id since we don't have a method to fetch user details
    return UserResponse(id=current_user_id, email="placeholder@example.com")  # This is a placeholder