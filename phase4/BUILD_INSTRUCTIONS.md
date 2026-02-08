# Docker Build Instructions

## Prerequisites
- Docker Desktop installed and running
- Stable internet connection
- Environment files configured

## Network Issue Troubleshooting

If you encounter network timeout errors, try these steps:

1. **Check Docker Desktop Status**
   ```bash
   docker info
   ```

2. **Restart Docker Desktop**
   - Close Docker Desktop completely
   - Restart it and wait for it to fully initialize

3. **Check Internet Connection**
   ```bash
   ping docker.io
   ```

4. **Configure Docker DNS** (if needed)
   - Open Docker Desktop Settings
   - Go to Docker Engine
   - Add DNS configuration:
   ```json
   {
     "dns": ["8.8.8.8", "8.8.4.4"]
   }
   ```

## Building Images Separately

### Backend Image
```bash
cd backend
docker build -t todo-backend:latest .
```

### Frontend Image
```bash
cd frontend
docker build -t todo-frontend:latest .
```

## Building with Docker Compose

### Build both images at once
```bash
docker-compose build
```

### Build specific service
```bash
docker-compose build backend
docker-compose build frontend
```

## Running the Application

### Start all services
```bash
docker-compose up -d
```

### Start specific service
```bash
docker-compose up -d backend
docker-compose up -d frontend
```

### View logs
```bash
docker-compose logs -f
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Stop services
```bash
docker-compose down
```

### Stop and remove volumes
```bash
docker-compose down -v
```

## Verify Images

### List built images
```bash
docker images | grep todo
```

Expected output:
```
todo-backend    latest    <image-id>    <time>    <size>
todo-frontend   latest    <image-id>    <time>    <size>
```

### Inspect image details
```bash
docker inspect todo-backend:latest
docker inspect todo-frontend:latest
```

## Running Containers Manually

### Backend
```bash
docker run -d \
  --name todo-backend \
  -p 8080:8080 \
  --env-file backend/.env \
  todo-backend:latest
```

### Frontend
```bash
docker run -d \
  --name todo-frontend \
  -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL=http://localhost:8080 \
  todo-frontend:latest
```

## Testing the Application

### Check backend health
```bash
curl http://localhost:8080/health
```

### Check frontend
```bash
curl http://localhost:3000
```

### Access the application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8080
- API Docs: http://localhost:8080/docs

## Cleanup

### Remove containers
```bash
docker rm -f todo-backend todo-frontend
```

### Remove images
```bash
docker rmi todo-backend:latest todo-frontend:latest
```

### Remove all unused Docker resources
```bash
docker system prune -a
```

## Production Deployment

### Tag images for registry
```bash
docker tag todo-backend:latest your-registry/todo-backend:v1.0.0
docker tag todo-frontend:latest your-registry/todo-frontend:v1.0.0
```

### Push to registry
```bash
docker push your-registry/todo-backend:v1.0.0
docker push your-registry/todo-frontend:v1.0.0
```

## Environment Variables

Make sure these files exist with proper values:

### backend/.env
```env
DATABASE_URL=postgresql+asyncpg://user:pass@host/db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
ENVIRONMENT=production
LOG_LEVEL=info
```

### frontend/.env.local (for local development)
```env
NEXT_PUBLIC_API_URL=http://localhost:8080
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8080
```

## Common Issues

### Issue: Port already in use
**Solution:** Stop the service using the port or change the port mapping
```bash
# Find process using port
netstat -ano | findstr :8080
# Kill process (Windows)
taskkill /PID <process-id> /F
```

### Issue: Build fails with "no space left on device"
**Solution:** Clean up Docker resources
```bash
docker system prune -a --volumes
```

### Issue: Container exits immediately
**Solution:** Check logs
```bash
docker logs todo-backend
docker logs todo-frontend
```
