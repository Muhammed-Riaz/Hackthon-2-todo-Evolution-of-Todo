"""
Main FastAPI application for the backend.
"""

import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# Use relative imports for the routes
from .api.v1.routes import tasks, auth, chat

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from contextlib import asynccontextmanager
from .models import *

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event manager to create database tables on startup.
    """
    from sqlmodel import SQLModel
    from .database.database import engine
    async with engine.begin() as conn:
        # Create all tables defined in the models
        await conn.run_sync(SQLModel.metadata.create_all)
    logger.info("Database tables created successfully")
    yield
    logger.info("Application shutdown")


# Create the FastAPI application with lifespan
app = FastAPI(
    title="Todo Backend API",
    description="Backend API for task management with user isolation",
    version="1.0.0",
    lifespan=lifespan
)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001", "http://127.0.0.1:3001"],  # Allow frontend origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)


# Middleware to log incoming requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"{request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# Include the auth, task, and chat routes
app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(chat.router)

@app.get("/")
def read_root():
    """
    Root endpoint for basic health check.
    """
    return {"message": "Todo Backend API is running"}

@app.get("/health")
def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy"}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler for the application.
    """
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error occurred"}
    )