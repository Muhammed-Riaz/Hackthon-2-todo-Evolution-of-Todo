"""
User service for the backend application.
Handles user-related operations like creation and authentication.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional
from passlib.context import CryptContext

from ..models.user_model import User
from ..schemas.auth_schemas import UserCreate


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Generate a hash for the given password.
    """
    return pwd_context.hash(password)


async def create_user(session: AsyncSession, user_create: UserCreate) -> User:
    """
    Create a new user with the provided details.
    """
    # Check if user already exists
    existing_user_query = select(User).where(User.email == user_create.email)
    result = await session.execute(existing_user_query)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash the password
    hashed_password = get_password_hash(user_create.password)

    # Create new user
    db_user = User(
        email=user_create.email,
        password_hash=hashed_password,
        first_name=user_create.first_name,
        last_name=user_create.last_name
    )

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return db_user


async def authenticate_user(session: AsyncSession, email: str, password: str) -> Optional[User]:
    """
    Authenticate a user by email and password.
    """
    # Find user by email
    user_query = select(User).where(User.email == email)
    result = await session.execute(user_query)
    user = result.scalar_one_or_none()

    if not user or not verify_password(password, user.password_hash):
        return None

    return user