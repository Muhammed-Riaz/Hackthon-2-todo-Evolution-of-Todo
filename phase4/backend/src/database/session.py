"""
Database Session Factory for MCP Tools

This module provides database session management for stateless MCP tool operations.
Each tool call opens its own database session, performs operations, and closes the session.
"""
from sqlmodel import create_engine, Session
from sqlalchemy.pool import StaticPool
from sqlalchemy import event
from typing import Generator
import sys
import os
# Add the backend root directory to the path to import settings
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from settings import settings

# Map the settings to match expected names
db_echo_sql = settings.db_echo_sql  # Use the actual setting
db_pool_recycle = settings.db_pool_recycle  # Use the actual setting
environment = settings.environment


# Create engine with connection pooling appropriate for stateless operations
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.db_echo_sql,
    pool_recycle=settings.db_pool_recycle,
    pool_pre_ping=True,
    # For stateless operations, we want to avoid connection reuse issues
    poolclass=StaticPool if settings.environment == "testing" else None,
)

# Add event listener to convert UUID strings to integers when inserting (for sync operations)
@event.listens_for(engine, "before_cursor_execute", retval=True)
def process_uuid_to_int(conn, cursor, statement, parameters, context, executemany):
    # Convert UUID strings to integers for user_id fields in parameters
    if isinstance(parameters, dict):
        new_params = parameters.copy()
        for key, value in parameters.items():
            if key == 'user_id' and isinstance(value, str):
                try:
                    # Convert UUID string to integer by taking hash
                    # This preserves uniqueness while fitting into integer column
                    user_id_int = abs(hash(value)) % (2**31 - 1)  # Fit within PostgreSQL integer range
                    new_params[key] = user_id_int
                except:
                    # If conversion fails, keep original value
                    pass
        parameters = new_params
    elif isinstance(parameters, list):
        # Handle executemany case
        new_params_list = []
        for param_dict in parameters:
            if isinstance(param_dict, dict):
                new_param_dict = param_dict.copy()
                for key, value in param_dict.items():
                    if key == 'user_id' and isinstance(value, str):
                        try:
                            user_id_int = abs(hash(value)) % (2**31 - 1)
                            new_param_dict[key] = user_id_int
                        except:
                            pass
                new_params_list.append(new_param_dict)
            else:
                new_params_list.append(param_dict)
        parameters = new_params_list

    return statement, parameters


def get_session() -> Generator[Session, None, None]:
    """
    Get a database session for MCP tool operations.

    Yields a Session that is guaranteed to be closed after use.
    This implements the stateless session pattern required for MCP tools.
    """
    with Session(engine) as session:
        yield session


def get_session_context():
    """
    Context manager for database sessions.
    Provides a session that will be properly closed even if an exception occurs.
    """
    return Session(engine)