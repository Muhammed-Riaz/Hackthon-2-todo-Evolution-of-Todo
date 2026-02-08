@echo off
echo ============================================
echo Docker Image Build Verification Script
echo ============================================
echo.

echo [1/5] Checking Docker Desktop status...
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker Desktop is not running!
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)
echo [OK] Docker Desktop is running

echo.
echo [2/5] Testing DNS resolution...
nslookup registry-1.docker.io >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] DNS resolution is failing!
    echo.
    echo SOLUTION: Configure Docker Desktop DNS
    echo 1. Open Docker Desktop Settings
    echo 2. Go to Docker Engine
    echo 3. Add: "dns": ["8.8.8.8", "8.8.4.4"]
    echo 4. Click Apply and Restart
    echo.
    echo Run fix-docker-dns.bat for step-by-step guide
    pause
    exit /b 1
)
echo [OK] DNS resolution is working

echo.
echo [3/5] Testing Docker Hub connectivity...
docker pull hello-world >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Cannot connect to Docker Hub!
    echo Please check your internet connection and DNS settings.
    pause
    exit /b 1
)
echo [OK] Docker Hub is accessible

echo.
echo [4/5] Checking if images already exist...
docker images | findstr "todo-backend" >nul 2>&1
if %errorlevel% equ 0 (
    echo [INFO] todo-backend image already exists
) else (
    echo [INFO] todo-backend image not found - will build
)

docker images | findstr "todo-frontend" >nul 2>&1
if %errorlevel% equ 0 (
    echo [INFO] todo-frontend image already exists
) else (
    echo [INFO] todo-frontend image not found - will build
)

echo.
echo [5/5] All checks passed!
echo.
echo ============================================
echo Ready to build Docker images separately
echo ============================================
echo.
echo You can now run: build-images.bat
echo.
pause
