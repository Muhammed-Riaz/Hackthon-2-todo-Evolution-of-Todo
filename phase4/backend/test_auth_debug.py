#!/usr/bin/env python3
"""
Simple test script to debug the authentication issue
"""

import asyncio
import json
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

# Import the problematic function
from src.services.user_service import authenticate_user

# Import the database session
from src.database.database import get_async_session

async def test_authentication():
    """Test the authentication function directly"""
    print("Testing authentication function...")
    
    # Get a database session
    session_gen = get_async_session()
    session = await session_gen.__anext__()
    
    try:
        # Try to authenticate the test user
        user = await authenticate_user(session, "test@example.com", "password123")
        print(f"Authentication result: {user}")
        
        if user:
            print(f"User authenticated successfully: {user.email}")
        else:
            print("Authentication failed - user not found or incorrect password")
            
    except Exception as e:
        print(f"Error during authentication: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await session.close()

if __name__ == "__main__":
    asyncio.run(test_authentication())