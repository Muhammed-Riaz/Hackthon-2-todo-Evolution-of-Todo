"""
Chat service for handling AI-powered conversations and MCP tool integration.
"""
import asyncio
import json
from typing import Dict, Any, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from datetime import datetime
import re

from ..models.conversation_model import Conversation, Message
from ..schemas.conversation_schemas import ConversationCreate


async def process_chat_message(
    session: AsyncSession,
    user_id: str,
    message: str,
    conversation_id: Optional[int] = None
) -> Dict[str, Any]:
    """
    Process a chat message by interacting with AI agent and potentially executing MCP tools.

    Args:
        session: Database session
        user_id: ID of the authenticated user
        message: User's input message
        conversation_id: Existing conversation ID (if any)

    Returns:
        Dictionary containing response, conversation_id, and any tool calls
    """
    # First, let's handle the conversation management
    if conversation_id is None:
        # Create a new conversation
        conversation = Conversation(
            user_id=user_id,
            title=message[:50] + "..." if len(message) > 50 else message  # Use first 50 chars as title
        )
        session.add(conversation)
        await session.flush()  # This assigns an ID to the conversation
        conversation_id = conversation.id
    else:
        # Verify conversation belongs to user
        existing_conversation = await session.get(Conversation, conversation_id)
        if not existing_conversation or str(existing_conversation.user_id) != str(user_id):
            raise ValueError("Conversation not found or doesn't belong to user")

    # Save user message to database
    user_message = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        role="user",
        content=message,
        timestamp=datetime.utcnow()
    )
    session.add(user_message)
    await session.flush()

    # Determine if the message contains a task operation
    # This is a simplified version - in reality, you'd use an AI agent
    response_text = ""
    tool_calls = []

    # Simple keyword-based task detection (would be AI in real impl)
    lowered_msg = message.lower()

    if any(word in lowered_msg for word in ["add", "create", "make", "new"]):
        if any(word in lowered_msg for word in ["task", "todo", "do", "buy"]):
            # This looks like a task creation request
            # Extract task information using improved parsing (would be AI in real impl)
            
            # Look for the task description after common verbs
            task_patterns = [
                r"add (?:a |)(?:task |to |)(.+?)(?:\.|!|\?|$)",
                r"create (?:a |)(?:task |to |)(.+?)(?:\.|!|\?|$)",
                r"make (?:a |)(?:task |to |)(.+?)(?:\.|!|\?|$)",
                r"buy *(.+?)(?:\.|!|\?|$)",
                r"get *(.+?)(?:\.|!|\?|$)",
                r"need to *(.+?)(?:\.|!|\?|$)",
                r"want to *(.+?)(?:\.|!|\?|$)"
            ]

            task_title = "New task"
            for pattern in task_patterns:  # Fixed variable name
                task_match = re.search(pattern, message.lower())
                if task_match:
                    task_title = task_match.group(1).strip()
                    break

            if task_title == "New task":
                # If no specific pattern matched, use the entire message or part of it
                task_title = message.replace("add ", "").replace("to ", "").replace("buy ", "").replace("get ", "").replace("need to ", "").replace("want to ", "").strip()

            # Actually execute the task creation instead of just simulating it
            from .task_service import create_task
            from ..schemas.task_schemas import TaskCreate
            
            try:
                task_create_obj = TaskCreate(
                    title=task_title,
                    description=f"Created from chat: {message}",
                    completed=False,
                    user_id=user_id
                )
                created_task = await create_task(session, task_create_obj)
                
                # Flush and commit the session to ensure the task is saved to the database
                await session.flush()
                await session.commit()
                
                # Verify the task was created by fetching it
                from sqlalchemy import select
                from ..models.task_model import Task
                stmt = select(Task).where(Task.title == task_title, Task.user_id == user_id)
                result = await session.execute(stmt)
                task_check = result.scalar_one_or_none()
                
                if task_check:
                    print(f"DEBUG: Task '{task_title}' successfully created with ID {task_check.id}")
                else:
                    print(f"DEBUG: Task '{task_title}' was not found after creation")
                
                tool_calls.append({
                    "name": "add_task",
                    "arguments": {"title": task_title, "description": f"Created from chat: {message}", "user_id": user_id}
                })
                response_text = f"I've created a task for '{task_title}'. It's been added to your task list!"
            except Exception as e:
                print(f"DEBUG: Error creating task: {e}")
                import traceback
                traceback.print_exc()
                await session.rollback()  # Rollback on error
                raise

    elif any(word in lowered_msg for word in ["complete", "done", "finish", "mark"]):
        if any(word in lowered_msg for word in ["task", "todo"]):
            # This looks like a task completion request
            # Extract task info (would be AI in real impl)
            tool_calls.append({
                "name": "complete_task",
                "arguments": {"user_id": user_id, "description": "Task completion requested from chat"}
            })
            response_text = "I'll help you complete that task. Could you please specify which task you'd like to mark as done?"

    elif any(word in lowered_msg for word in ["show", "list", "view", "get"]):
        if any(word in lowered_msg for word in ["task", "todo", "my"]):
            # This looks like a task listing request
            tool_calls.append({
                "name": "list_tasks",
                "arguments": {"user_id": user_id}
            })
            response_text = "I'll fetch your tasks for you."

    elif any(word in lowered_msg for word in ["delete", "remove", "cancel"]):
        if any(word in lowered_msg for word in ["task", "todo"]):
            # This looks like a task deletion request
            response_text = "I can help you delete a task. Please specify which task you'd like to remove."
            tool_calls.append({
                "name": "delete_task",
                "arguments": {"user_id": user_id, "description": "Task deletion requested from chat"}
            })

    else:
        # Default response for general conversation
        response_text = f"I understand you said: '{message}'. I can help you manage your tasks. Try saying things like 'Add a task to buy groceries' or 'Show my tasks'."

    # Save assistant response to database
    assistant_message = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        role="assistant",
        content=response_text,
        timestamp=datetime.utcnow()
    )
    session.add(assistant_message)
    await session.commit()

    timestamp_iso = datetime.utcnow().isoformat()
    return {
        "response": response_text,
        "conversation_id": conversation_id,
        "tool_calls": tool_calls,
        "timestamp": timestamp_iso
    }


async def get_conversation_history(
    session: AsyncSession,
    user_id: str,
    conversation_id: int
) -> List[Dict[str, Any]]:
    """
    Retrieve the history of messages in a conversation.
    """
    from sqlalchemy import select

    # Verify conversation belongs to user
    conversation = await session.get(Conversation, conversation_id)
    if not conversation or str(conversation.user_id) != str(user_id):
        raise ValueError("Conversation not found or doesn't belong to user")

    # Get all messages in the conversation
    stmt = select(Message).where(
        Message.conversation_id == conversation_id
    ).order_by(Message.timestamp.asc())

    messages = await session.execute(stmt)
    message_list = []

    for msg in messages.scalars():
        message_list.append({
            "role": msg.role,
            "content": msg.content,
            "timestamp": msg.timestamp.isoformat()
        })

    return message_list