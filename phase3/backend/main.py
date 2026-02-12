from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Import routers
# from api.v1.routers import tasks, auth, chat
from src.api.v1.routes import tasks, auth, chat


app = FastAPI(title="Todo API", version="1.0.0")

# CORS middleware - Allow production and development origins
allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
    "https://hackthon-2-todo-evolution-of-todo-b.vercel.app",  # Your Vercel production URL
]

# In development, allow all origins for testing
if os.getenv("ENVIRONMENT") == "development":
    allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(tasks.router, prefix="/api", tags=["tasks"])
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(chat.router, prefix="/api", tags=["chat"])

@app.get("/")
def read_root():
    return {"message": "Todo API v1"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}