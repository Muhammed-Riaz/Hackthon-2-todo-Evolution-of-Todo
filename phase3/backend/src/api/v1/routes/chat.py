"""
Chat API routes for the backend application.
Integrates with AI agent for natural language processing and MCP tools.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
import uuid
import json
from datetime import datetime

from ....database.database import get_async_session
from ....auth.dependencies import get_current_user_id
from ....services.chat_service import process_chat_message
from ....schemas.conversation_schemas import ChatRequest, ChatResponse


router = APIRouter(prefix="/{user_id}", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    user_id: str,
    chat_request: ChatRequest,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Handle chat messages and process natural language requests.
    Integrates with AI agent and MCP tools for task operations.
    """
    # Ensure the user_id in the request matches the user_id in the token
    if current_user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="User ID in token does not match user ID in URL"
        )

    # Validate message content
    if not chat_request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message content is required"
        )

    try:
        # Process the chat message using the chat service
        # This will integrate with the AI agent and MCP tools
        from ....services.chat_service import process_chat_message
        response = await process_chat_message(
            session=session,
            user_id=current_user_id,
            message=chat_request.message,
            conversation_id=chat_request.conversation_id
        )

        # Commit the session to ensure any database changes are saved
        await session.commit()

        from datetime import datetime
        timestamp_str = response.get("timestamp")
        if isinstance(timestamp_str, str):
            # Parse ISO format datetime string
            try:
                # Handle different datetime formats
                timestamp_str_clean = timestamp_str.replace('Z', '+00:00')
                if timestamp_str_clean.endswith('+00:00'):
                    timestamp = datetime.fromisoformat(timestamp_str_clean)
                else:
                    timestamp = datetime.fromisoformat(timestamp_str_clean)
            except ValueError:
                # If parsing fails, use current time
                timestamp = datetime.utcnow()
        else:
            timestamp = datetime.utcnow()

        # Ensure conversation_id is an integer
        conv_id = response.get("conversation_id")
        if conv_id is not None:
            try:
                conv_id = int(conv_id)
            except (ValueError, TypeError):
                conv_id = 1  # Default to 1 if conversion fails

        return ChatResponse(
            response=response.get("response", ""),
            conversation_id=conv_id,
            tool_calls=response.get("tool_calls", []),
            timestamp=timestamp
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat message: {str(e)}"
        )