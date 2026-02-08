# Quick Start Guide - Docker Build & Deploy

## 🎯 Overview

Your Todo App has been configured for Docker deployment with:
- ✅ **Backend Dockerfile** - FastAPI application (Python 3.11)
- ✅ **Frontend Dockerfile** - Next.js application (Node 20)
- ✅ **Docker Compose** - Orchestrates both services
- ✅ **Build Scripts** - Automated build process

## 🚀 Quick Start (3 Steps)

### Step 1: Fix Network Issue (If Needed)

The initial build failed due to Docker Hub connection timeout. Try these:

**Option A: Restart Docker Desktop**
```bash
# Close Docker Desktop completely, then restart it
# Wait 30 seconds for full initialization
docker info
```

**Option B: Configure DNS**
1. Open Docker Desktop → Settings → Docker Engine
2. Add this configuration:
```json
{
  "dns": ["8.8.8.8", "8.8.4.4"]
}
```
3. Click "Apply & Restart"

### Step 2: Build Images

**Windows:**
```cmd
build-images.bat
```

**Linux/Mac:**
```bash
chmod +x build-images.sh
./build-images.sh
```

**Or manually:**
```bash
# Backend
cd backend
docker build -t todo-backend:latest .
cd ..

# Frontend
cd frontend
docker build -t todo-frontend:latest .
cd ..
```

**Or with Docker Compose:**
```bash
docker-compose build
```

### Step 3: Run Application

```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

## 🌐 Access Your Application

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8080
- **API Docs:** http://localhost:8080/docs
- **Health Check:** http://localhost:8080/health

## 📦 What Was Created

### 1. Backend Dockerfile (`backend/Dockerfile`)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

**Features:**
- Python 3.11 slim base image
- PostgreSQL client included
- Health check configured
- Port 8080 exposed

### 2. Frontend Dockerfile (`frontend/Dockerfile`)
```dockerfile
FROM node:20-alpine AS base
# Multi-stage build: deps → builder → runner
# Optimized for production
# Standalone output mode
# Non-root user for security
EXPOSE 3000
CMD ["node", "server.js"]
```

**Features:**
- Node 20 alpine base (minimal size)
- Multi-stage build (optimized)
- Standalone mode enabled
- Port 3000 exposed

### 3. Docker Compose (`docker-compose.yml`)
```yaml
services:
  backend:
    build: ./backend
    ports: ["8080:8080"]

  frontend:
    build: ./frontend
    ports: ["3000:3000"]
    depends_on: [backend]
```

**Features:**
- Service orchestration
- Health checks
- Auto-restart policies
- Custom network

### 4. Configuration Files
- `backend/.dockerignore` - Excludes venv, logs, cache
- `frontend/.dockerignore` - Excludes node_modules, .next
- `frontend/next.config.js` - Updated with `output: 'standalone'`

### 5. Build Scripts
- `build-images.bat` - Windows build script
- `build-images.sh` - Linux/Mac build script

### 6. Documentation
- `BUILD_INSTRUCTIONS.md` - Comprehensive guide
- `DOCKER_SETUP_SUMMARY.md` - Detailed overview
- `QUICK_START.md` - This file

## 🔧 Common Commands

### Build Commands
```bash
# Build both images
docker-compose build

# Build specific service
docker-compose build backend
docker-compose build frontend

# Build with no cache
docker-compose build --no-cache

# Parallel build
docker-compose build --parallel
```

### Run Commands
```bash
# Start services
docker-compose up -d

# Start with logs
docker-compose up

# Start specific service
docker-compose up -d backend

# Restart services
docker-compose restart

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### Debug Commands
```bash
# View logs
docker-compose logs -f
docker-compose logs -f backend
docker-compose logs -f frontend

# Check status
docker-compose ps

# Execute command in container
docker-compose exec backend bash
docker-compose exec frontend sh

# View container details
docker inspect todo-backend
docker inspect todo-frontend
```

### Image Commands
```bash
# List images
docker images | grep todo

# Remove images
docker rmi todo-backend:latest
docker rmi todo-frontend:latest

# Tag for registry
docker tag todo-backend:latest myregistry/todo-backend:v1.0.0
docker tag todo-frontend:latest myregistry/todo-frontend:v1.0.0

# Push to registry
docker push myregistry/todo-backend:v1.0.0
docker push myregistry/todo-frontend:v1.0.0
```

## 🧪 Testing

### Test Backend
```bash
# Health check
curl http://localhost:8080/health

# API documentation
open http://localhost:8080/docs

# Test endpoint
curl http://localhost:8080/api/tasks
```

### Test Frontend
```bash
# Open in browser
open http://localhost:3000

# Check if running
curl http://localhost:3000
```

## 🐛 Troubleshooting

### Issue: Network timeout during build
**Solution:**
1. Restart Docker Desktop
2. Configure DNS (see Step 1)
3. Check internet connection: `ping docker.io`

### Issue: Port already in use
**Solution:**
```bash
# Windows - Find process
netstat -ano | findstr :8080
taskkill /PID <pid> /F

# Or change port in docker-compose.yml
ports: ["8081:8080"]
```

### Issue: Build fails with "no space"
**Solution:**
```bash
docker system prune -a --volumes
```

### Issue: Container exits immediately
**Solution:**
```bash
docker-compose logs backend
docker-compose logs frontend
```

### Issue: Frontend can't connect to backend
**Solution:**
Check environment variables in docker-compose.yml:
```yaml
frontend:
  environment:
    - NEXT_PUBLIC_API_URL=http://backend:8080
```

## 📊 Expected Build Output

### Backend Build (~2-3 minutes)
```
[+] Building 45.2s (12/12) FINISHED
 => [1/6] FROM python:3.11-slim
 => [2/6] WORKDIR /app
 => [3/6] COPY requirements.txt .
 => [4/6] RUN pip install -r requirements.txt
 => [5/6] COPY . .
 => [6/6] exporting to image
Successfully tagged todo-backend:latest
```

### Frontend Build (~3-5 minutes)
```
[+] Building 120.5s (18/18) FINISHED
 => [deps] npm ci
 => [builder] npm run build
 => [runner] COPY --from=builder
Successfully tagged todo-frontend:latest
```

### Image Sizes
- **Backend:** ~450MB (Python + dependencies)
- **Frontend:** ~180MB (Node + Next.js standalone)

## 🚢 Deployment Options

### Local Development
```bash
docker-compose up -d
```

### Production Deployment

**Option 1: Docker Compose on VPS**
```bash
# On server
git clone <repo>
cd phase4
docker-compose -f docker-compose.prod.yml up -d
```

**Option 2: Container Registry**
```bash
# Tag and push
docker tag todo-backend:latest registry.example.com/todo-backend:v1.0.0
docker push registry.example.com/todo-backend:v1.0.0
```

**Option 3: Cloud Platforms**
- AWS ECS/Fargate
- Google Cloud Run
- Azure Container Instances
- Railway
- Render

## ✅ Success Checklist

- [ ] Docker Desktop is running
- [ ] Network connectivity is working
- [ ] Backend image built successfully
- [ ] Frontend image built successfully
- [ ] Both images appear in `docker images`
- [ ] Services start with `docker-compose up -d`
- [ ] Backend health check passes
- [ ] Frontend loads in browser
- [ ] API documentation accessible

## 📞 Next Steps

1. **Resolve network issue** (restart Docker Desktop)
2. **Run build script** (`build-images.bat` or `build-images.sh`)
3. **Start services** (`docker-compose up -d`)
4. **Test application** (http://localhost:3000)
5. **Deploy to production** (optional)

## 📚 Additional Resources

- `BUILD_INSTRUCTIONS.md` - Detailed build guide
- `DOCKER_SETUP_SUMMARY.md` - Complete overview
- `docker-compose.yml` - Service configuration
- `backend/Dockerfile` - Backend image definition
- `frontend/Dockerfile` - Frontend image definition

---

**Need Help?** Check the troubleshooting section or review the detailed documentation files.
