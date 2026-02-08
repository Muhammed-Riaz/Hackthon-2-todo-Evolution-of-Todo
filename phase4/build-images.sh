#!/bin/bash

# Build script for Todo App Docker images

echo "========================================"
echo "Building Todo App Docker Images"
echo "========================================"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "ERROR: Docker is not running!"
    echo "Please start Docker Desktop and try again."
    exit 1
fi

echo "[1/4] Docker is running..."
echo ""

# Build Backend Image
echo "[2/4] Building Backend Image..."
echo "----------------------------------------"
cd backend || exit 1
docker build -t todo-backend:latest .
if [ $? -ne 0 ]; then
    echo "ERROR: Backend build failed!"
    cd ..
    exit 1
fi
cd ..
echo "Backend image built successfully!"
echo ""

# Build Frontend Image
echo "[3/4] Building Frontend Image..."
echo "----------------------------------------"
cd frontend || exit 1
docker build -t todo-frontend:latest .
if [ $? -ne 0 ]; then
    echo "ERROR: Frontend build failed!"
    cd ..
    exit 1
fi
cd ..
echo "Frontend image built successfully!"
echo ""

# List built images
echo "[4/4] Verifying Images..."
echo "----------------------------------------"
docker images | grep todo
echo ""

echo "========================================"
echo "Build Complete!"
echo "========================================"
echo ""
echo "Images created:"
echo "  - todo-backend:latest"
echo "  - todo-frontend:latest"
echo ""
echo "Next steps:"
echo "  1. Run: docker-compose up -d"
echo "  2. Access frontend: http://localhost:3000"
echo "  3. Access backend: http://localhost:8080"
echo ""
