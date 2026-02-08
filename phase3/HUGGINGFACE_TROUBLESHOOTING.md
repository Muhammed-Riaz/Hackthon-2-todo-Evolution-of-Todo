# Hugging Face Backend Troubleshooting Guide

## Quick Diagnosis

Your backend at https://riaz110-phase3.hf.space is returning 503 (Service Unavailable).

## Common Causes & Solutions

### 1. Check Space Status
Visit: https://huggingface.co/spaces/riaz110/phase3
- Look for error messages in the logs
- Check if the Space is "Building" or "Running"

### 2. Port Configuration Issue (Most Common)

Hugging Face expects your app to run on port **7860** by default.

**Fix**: Update your backend startup command:

In your `Dockerfile` or startup script, change:
```bash
# Wrong (for local development)
uvicorn main:app --host 0.0.0.0 --port 8080

# Correct (for Hugging Face)
uvicorn main:app --host 0.0.0.0 --port 7860
```

Or create a `start.sh` file:
```bash
#!/bin/bash
uvicorn main:app --host 0.0.0.0 --port 7860
```

### 3. Missing Environment Variables

Go to Space Settings → Variables and add:
```
DATABASE_URL=postgresql+asyncpg://neondb_owner:npg_KzNuXVCp2RB5@ep-dark-union-ahj01ro8-pooler.c-3.us-east-1.aws.neon.tech/neondb
SECRET_KEY=n34_axppdz3mO2qxH5jUdwXj0JFzj09logjcHZfzfLs
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
ENVIRONMENT=production
```

### 4. Check requirements.txt

Ensure all dependencies are listed:
```
fastapi
uvicorn[standard]
sqlmodel
sqlalchemy
asyncpg
pydantic
pydantic-settings
passlib[bcrypt]
bcrypt
python-jose[cryptography]
cryptography
python-multipart
python-dotenv
httpx
requests
psycopg2-binary
alembic
```

### 5. CORS Configuration

Make sure your `main.py` has CORS configured:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For testing, restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Testing Steps

After making changes:

1. **Rebuild the Space** (it should auto-rebuild on file changes)
2. **Wait 2-3 minutes** for the build to complete
3. **Test the health endpoint**:
   ```bash
   curl https://riaz110-phase3.hf.space/health
   ```
   Should return: `{"status":"healthy"}`

4. **Test the root endpoint**:
   ```bash
   curl https://riaz110-phase3.hf.space/
   ```
   Should return: `{"message":"Todo API v1"}`

## Quick Fix Checklist

- [ ] Port is set to 7860
- [ ] All environment variables are set
- [ ] requirements.txt includes all dependencies
- [ ] CORS is configured
- [ ] Space is in "Running" state (not "Building" or "Error")
- [ ] /health endpoint returns 200 OK
- [ ] Logs show "Application startup complete"

## Once Backend is Working

Run this test:
```bash
# Test health endpoint
curl https://riaz110-phase3.hf.space/health

# Test signup (should create a user)
curl -X POST https://riaz110-phase3.hf.space/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!","first_name":"Test","last_name":"User"}'
```

If both work, you're ready to deploy to Vercel!
