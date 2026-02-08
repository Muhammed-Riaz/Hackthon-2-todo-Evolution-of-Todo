# Quickstart Guide: Authentication & API Security

**Feature**: 002-auth-security-jwt

## Setup Instructions

### Prerequisites
- Node.js 18+ (for frontend with Better Auth)
- Python 3.11+ (for backend with FastAPI)
- pip package manager
- Git
- Existing Spec 1 backend setup

### Frontend Setup (Next.js + Better Auth)

1. **Install Better Auth**:
   ```bash
   cd frontend
   npm install better-auth
   ```

2. **Configure Better Auth with JWT plugin**:
   ```javascript
   // frontend/lib/auth.js
   import { betterAuth } from "better-auth";
   import { jwt } from "better-auth/plugins";

   export const auth = betterAuth({
     app: {
       name: "Todo App",
       baseUrl: process.env.NEXT_PUBLIC_BASE_URL || "http://localhost:3000"
     },
     secret: process.env.BETTER_AUTH_SECRET,
     plugins: [
       jwt({
         secret: process.env.BETTER_AUTH_SECRET,
         expiresIn: "7d",  // 7 days expiration
       })
     ]
   });
   ```

3. **Set up environment variables**:
   ```bash
   # frontend/.env.local
   NEXT_PUBLIC_BASE_URL=http://localhost:3000
   BETTER_AUTH_SECRET=your-super-secret-key-here
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

4. **Create API client with JWT injection**:
   ```javascript
   // frontend/services/api-client.js
   import { getJwt } from "better-auth/client";

   class ApiClient {
     constructor(baseURL) {
       this.baseURL = baseURL;
     }

     async request(endpoint, options = {}) {
       const token = getJwt();  // Get JWT token from Better Auth
       const headers = {
         'Content-Type': 'application/json',
         ...options.headers,
       };

       if (token) {
         headers['Authorization'] = `Bearer ${token}`;
       }

       const response = await fetch(`${this.baseURL}${endpoint}`, {
         ...options,
         headers,
       });

       if (!response.ok) {
         throw new Error(`HTTP error! status: ${response.status}`);
       }

       return response.json();
     }

     // Convenience methods
     async get(endpoint) {
       return this.request(endpoint, { method: 'GET' });
     }

     async post(endpoint, data) {
       return this.request(endpoint, {
         method: 'POST',
         body: JSON.stringify(data),
       });
     }

     async put(endpoint, data) {
       return this.request(endpoint, {
         method: 'PUT',
         body: JSON.stringify(data),
       });
     }

     async patch(endpoint, data) {
       return this.request(endpoint, {
         method: 'PATCH',
         body: JSON.stringify(data),
       });
     }

     async delete(endpoint) {
       return this.request(endpoint, { method: 'DELETE' });
     }
   }

   export const api = new ApiClient(process.env.NEXT_PUBLIC_API_URL);
   ```

### Backend Setup (FastAPI + JWT Verification)

1. **Install required dependencies**:
   ```bash
   cd backend
   pip install python-jose[cryptography] python-multipart
   ```

2. **Update requirements.txt**:
   ```txt
   fastapi==0.104.1
   sqlmodel==0.0.16
   uvicorn[standard]==0.24.0
   psycopg2-binary==2.9.9
   pydantic-settings==2.1.0
   alembic==1.13.1
   python-multipart==0.0.6
   python-jose[cryptography]==3.3.0  # Add this for JWT handling
   ```

3. **Create JWT utility functions**:
   ```python
   # backend/src/auth/jwt.py
   from datetime import datetime, timedelta
   from typing import Optional
   from jose import JWTError, jwt
   from fastapi import HTTPException, status
   from ..core.config import get_settings

   settings = get_settings()

   def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
       to_encode = data.copy()
       if expires_delta:
           expire = datetime.utcnow() + expires_delta
       else:
           expire = datetime.utcnow() + timedelta(minutes=15)

       to_encode.update({"exp": expire})
       encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
       return encoded_jwt

   def verify_token(token: str) -> Optional[dict]:
       try:
           payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
           user_id: str = payload.get("sub")
           if user_id is None:
               return None
           return payload
       except JWTError:
           return None
   ```

4. **Create auth dependencies**:
   ```python
   # backend/src/auth/dependencies.py
   from fastapi import Depends, HTTPException, status
   from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
   from .jwt import verify_token

   security = HTTPBearer()

   async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
       token = credentials.credentials
       user_payload = verify_token(token)
       if user_payload is None:
           raise HTTPException(
               status_code=status.HTTP_401_UNAUTHORIZED,
               detail="Could not validate credentials",
               headers={"WWW-Authenticate": "Bearer"},
           )
       return user_payload
   ```

5. **Update configuration**:
   ```python
   # backend/src/core/config.py (updated)
   from pydantic_settings import BaseSettings
   from typing import Optional


   class Settings(BaseSettings):
       database_url: str = "postgresql+psycopg2://user:password@localhost/dbname"
       environment: str = "development"
       log_level: str = "info"
       secret_key: str = "your-secret-key-here"  # Should match BETTER_AUTH_SECRET
       algorithm: str = "HS256"
       access_token_expire_minutes: int = 60 * 24 * 7  # 7 days

       class Config:
           env_file = ".env"
           env_file_encoding = 'utf-8'


   def get_settings() -> Settings:
       return Settings()
   ```

6. **Update main.py to include auth dependencies**:
   ```python
   # backend/src/main.py (updated)
   import logging
   from fastapi import FastAPI, Request
   from fastapi.responses import JSONResponse
   from .api.v1.routes import tasks

   # Configure logging
   logging.basicConfig(level=logging.INFO)
   logger = logging.getLogger(__name__)

   # Create the FastAPI application
   app = FastAPI(
       title="Todo Backend API",
       description="Backend API for task management with user isolation",
       version="1.0.0"
   )

   # Middleware to log incoming requests
   @app.middleware("http")
   async def log_requests(request: Request, call_next):
       logger.info(f"{request.method} {request.url}")
       response = await call_next(request)
       logger.info(f"Response status: {response.status_code}")
       return response

   # Include the task routes
   app.include_router(tasks.router)

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
   ```

7. **Update .env.example**:
   ```bash
   # backend/.env.example
   # Database configuration
   DATABASE_URL=postgresql+psycopg2://username:password@localhost:5432/todo_db

   # JWT Secret (must match BETTER_AUTH_SECRET in frontend)
   SECRET_KEY=your-super-secret-key-here

   # Algorithm for JWT
   ALGORITHM=HS256

   # Access token expiration in minutes (default: 7 days = 10080 minutes)
   ACCESS_TOKEN_EXPIRE_MINUTES=10080

   # Environment (development, staging, production)
   ENVIRONMENT=development

   # Log level (debug, info, warning, error)
   LOG_LEVEL=info
   ```

## Testing the Authentication System

### Manual Testing Steps

1. **Register a new user**:
   ```bash
   curl -X POST "http://localhost:3000/api/auth/register" \
     -H "Content-Type: application/json" \
     -d '{"email": "test@example.com", "password": "securepassword", "name": "Test User"}'
   ```

2. **Login to get JWT token**:
   ```bash
   curl -X POST "http://localhost:3000/api/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"email": "test@example.com", "password": "securepassword"}'
   ```

3. **Use JWT token to access protected endpoints**:
   ```bash
   # Replace YOUR_JWT_TOKEN with the token from login response
   curl -X GET "http://localhost:8000/api/user123/tasks" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN"
   ```

4. **Test unauthorized access**:
   ```bash
   # Should return 401 Unauthorized
   curl -X GET "http://localhost:8000/api/user123/tasks"
   # (without Authorization header)
   ```

5. **Test cross-user access prevention**:
   ```bash
   # Should return 403 Forbidden if JWT user_id doesn't match URL user_id
   curl -X GET "http://localhost:8000/api/different_user/tasks" \
     -H "Authorization: Bearer VALID_JWT_TOKEN_BUT_DIFFERENT_USER"
   ```

## Verification Steps

1. User registration and login work correctly
2. JWT tokens are properly issued and validated
3. All API endpoints require valid JWT tokens
4. User data isolation is enforced (users can only access their own tasks)
5. Cross-user access attempts are properly blocked
6. Expired tokens are rejected
7. Invalid tokens return appropriate error responses