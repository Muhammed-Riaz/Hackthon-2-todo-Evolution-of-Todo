@echo off
REM Build script for Todo App Docker images

echo ========================================
echo Building Todo App Docker Images
echo ========================================
echo.

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker is not running!
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)

echo [1/4] Docker is running...
echo.

REM Build Backend Image
echo [2/4] Building Backend Image...
echo ----------------------------------------
cd backend
docker build -t todo-backend:latest .
if %errorlevel% neq 0 (
    echo ERROR: Backend build failed!
    cd ..
    pause
    exit /b 1
)
cd ..
echo Backend image built successfully!
echo.

REM Build Frontend Image
echo [3/4] Building Frontend Image...
echo ----------------------------------------
cd frontend
docker build -t todo-frontend:latest .
if %errorlevel% neq 0 (
    echo ERROR: Frontend build failed!
    cd ..
    pause
    exit /b 1
)
cd ..
echo Frontend image built successfully!
echo.

REM List built images
echo [4/4] Verifying Images...
echo ----------------------------------------
docker images | findstr todo
echo.

echo ========================================
echo Build Complete!
echo ========================================
echo.
echo Images created:
echo   - todo-backend:latest
echo   - todo-frontend:latest
echo.
echo Next steps:
echo   1. Run: docker-compose up -d
echo   2. Access frontend: http://localhost:3000
echo   3. Access backend: http://localhost:8080
echo.
pause
