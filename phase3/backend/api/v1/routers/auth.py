from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlmodel import Session, select
from datetime import timedelta
from models.user_task_models import User, UserRole
from utils.auth import hash_password, verify_password, create_access_token, get_current_user
from database import get_session_dep
from settings import settings
from typing import Optional


router = APIRouter()


@router.post("/auth/register")
async def register_user(
    email: str,
    password: str,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    session: Session = Depends(get_session_dep)
):
    """Register a new user"""
    # Check if user already exists
    existing_user = session.exec(select(User).where(User.email == email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash the password
    hashed_password = hash_password(password)

    # Create new user
    user = User(
        email=email,
        password_hash=hashed_password,
        first_name=first_name,
        last_name=last_name,
        role=UserRole.USER
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        }
    }


@router.post("/auth/login")
async def login_user(
    username: str = Form(...),
    password: str = Form(...),
    session: Session = Depends(get_session_dep)
):
    """Login a user and return an access token"""
    # Find user by email
    user = session.exec(select(User).where(User.email == username)).first()

    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        }
    }


@router.get("/auth/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return current_user


@router.post("/auth/logout")
async def logout_user():
    """Logout the current user"""
    # In a stateless JWT system, the server doesn't maintain session state
    # The client should remove the token from storage
    return {"message": "Successfully logged out"}