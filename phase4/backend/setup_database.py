#!/usr/bin/env python3
"""
Setup script for the Todo Backend Database
"""

import asyncio
from sqlmodel import SQLModel
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src.database.database import engine
from src.models.user_model import User
from src.models.task_model import Task
from src.models.conversation_model import Conversation
from src.models.base import BaseSQLModel, TimestampMixin


async def create_tables():
    """Create all database tables"""
    print("Creating database tables...")
    
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(SQLModel.metadata.create_all)
    
    print("Database tables created successfully!")


async def main():
    """Main setup function"""
    print("Setting up Todo Backend Database...")
    
    try:
        await create_tables()
        print("\nDatabase setup completed successfully!")
        print("You can now start the backend server with: uvicorn src.main:app --reload --port 8000")
    except Exception as e:
        print(f"Error during setup: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())