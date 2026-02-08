#!/usr/bin/env python3
"""
Simple test to verify that the models work with string user IDs
"""

import asyncio
from sqlmodel import select
from src.database.database import get_async_session, engine
from src.models.task_model import Task
from src.models.user_model import User
from contextlib import asynccontextmanager


async def test_models():
    """Test that models work with string user IDs"""
    print("Testing models with string user IDs...")
    
    # Create a test user and task
    from src.database.database import AsyncSessionLocal
    
    async with AsyncSessionLocal() as session:
        # Create a test user
        test_user = User(
            email="test@example.com",
            password_hash="hashed_password"
        )
        
        session.add(test_user)
        await session.commit()
        await session.refresh(test_user)
        
        print(f"Created user with ID: {test_user.id} (type: {type(test_user.id)})")
        
        # Create a test task for this user
        test_task = Task(
            title="Test Task",
            description="This is a test task",
            user_id=test_user.id  # Using the string user ID
        )
        
        session.add(test_task)
        await session.commit()
        await session.refresh(test_task)
        
        print(f"Created task with ID: {test_task.id}, user_id: {test_task.user_id} (type: {type(test_task.user_id)})")
        
        # Query the task by user_id
        statement = select(Task).where(Task.user_id == test_user.id)
        result = await session.execute(statement)
        tasks = result.scalars().all()
        
        print(f"Found {len(tasks)} tasks for user {test_user.id}")
        for task in tasks:
            print(f"  - Task: {task.title}")
    
    print("Test completed successfully!")


if __name__ == "__main__":
    asyncio.run(test_models())