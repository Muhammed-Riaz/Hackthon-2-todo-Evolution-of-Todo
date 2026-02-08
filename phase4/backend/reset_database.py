#!/usr/bin/env python3
"""
Database reset script for the Todo Backend
This script drops existing tables and recreates them with the correct schema
"""

import asyncio
from sqlmodel import SQLModel, text
from src.database.database import engine
from src.models.user_model import User
from src.models.task_model import Task
from src.models.conversation_model import Conversation
from src.models.base import BaseSQLModel, TimestampMixin


async def reset_database():
    """Drop and recreate all database tables"""
    print("Resetting database with correct schema...")
    
    async with engine.begin() as conn:
        # Drop all tables
        print("Dropping existing tables...")
        await conn.run_sync(SQLModel.metadata.drop_all)
        
        # Create all tables with correct schema
        print("Creating tables with correct schema...")
        await conn.run_sync(SQLModel.metadata.create_all)
    
    print("Database reset completed successfully!")
    print("Tables created with string user_id columns.")


if __name__ == "__main__":
    asyncio.run(reset_database())