from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Import routers
# from api.v1.routers import tasks, auth
from src.api.v1.routes import tasks, auth


app = FastAPI(title="Todo API", version="1.0.0")

# CORS middleware - in production, restrict origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Should be restricted in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(tasks.router, prefix="/api", tags=["tasks"])
app.include_router(auth.router, prefix="/api", tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "Todo API v1"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}