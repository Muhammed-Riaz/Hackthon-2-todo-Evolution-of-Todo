# JWT Auth Middleware Pattern Skill

**Name:** `jwt-auth-middleware-pattern`
**Description:** Standard JWT authentication & user extraction pattern for Phase 2 Todo app
**Version:** `1.0-phase2`

## Instructions

Apply this authentication pattern to ALL protected endpoints and API calls in Phase 2.

## Backend Implementation (FastAPI)

### JWT Configuration
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

# Shared secret - must match BETTER_AUTH_SECRET
SECRET_KEY = "BETTER_AUTH_SECRET"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
```

### Current User Dependency
```python
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Extract and verify JWT token, return user_id
    Raises 401 if token is invalid or missing
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")  # or payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
```

### Protected Endpoint Example
```python
@router.post("/tasks")
async def create_task(
    task_data: TaskCreate,
    current_user_id: str = Depends(get_current_user)  # Auto-injected user_id
):
    # current_user_id is guaranteed to be valid
    task = await create_task_in_db(
        title=task_data.title,
        description=task_data.description,
        user_id=current_user_id
    )
    return task
```

## Frontend Implementation (Next.js)

### Token Storage
```javascript
// Prefer httpOnly cookie for security
// Fallback to localStorage if cookies not available

// Set token (after login)
export function setAuthToken(token) {
  if (typeof document !== 'undefined') {
    document.cookie = `auth_token=${token}; path=/; Secure; SameSite=Strict`;
  }
}

// Get token
export function getAuthToken() {
  if (typeof document !== 'undefined') {
    const match = document.cookie.match(/auth_token=([^;]+)/);
    return match ? match[1] : null;
  }
  return null;
}
```

### API Client Wrapper
```javascript
import { getAuthToken } from './auth';

class ApiClient {
  constructor(baseUrl) {
    this.baseUrl = baseUrl;
  }

  async request(endpoint, options = {}) {
    const token = getAuthToken();
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${this.baseUrl}${endpoint}`, {
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
}

// Usage
export const api = new ApiClient(process.env.NEXT_PUBLIC_API_URL);
```

## Security Requirements

1. **Shared Secret**: Must use `BETTER_AUTH_SECRET` on both backend and frontend
2. **Token Storage**: Prefer httpOnly cookies over localStorage
3. **Token Transmission**: Always use HTTPS
4. **User Extraction**: user_id comes from JWT payload only
5. **Error Handling**: Return 401 for invalid/missing tokens

## Integration Points

- **Login**: Store JWT token after successful authentication
- **API Calls**: Automatically attach Authorization header
- **Protected Routes**: Use `get_current_user` dependency
- **Logout**: Clear token from storage

## Benefits

- **Consistent authentication** across all endpoints
- **Automatic user extraction** via dependency injection
- **Secure token handling** with httpOnly cookies
- **Clean API client** interface
- **Easy integration** with existing auth systems