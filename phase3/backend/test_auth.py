import asyncio
from src.services.user_service import create_user
from src.database.database import get_async_session
from src.models.user_model import User
from src.schemas.auth_schemas import UserCreate
from sqlalchemy.ext.asyncio import AsyncSession

async def test_user_creation():
    """Test user creation directly"""
    print("Testing user creation...")
    
    # Create a test user
    user_create = UserCreate(email="newuniqueuser@example.com", password="password123")
    
    # Get a database session
    session_gen = get_async_session()
    session = await session_gen.__anext__()
    
    try:
        # Try to create the user
        user = await create_user(session, user_create)
        print(f"User created successfully: {user}")
    except Exception as e:
        print(f"Error creating user: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await session.close()

if __name__ == "__main__":
    asyncio.run(test_user_creation())