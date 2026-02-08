@echo off
echo ============================================
echo Docker Desktop DNS Configuration Guide
echo ============================================
echo.
echo STEP 1: Open Docker Desktop
echo   - Click Docker icon in system tray
echo   - Click Settings (gear icon)
echo.
echo STEP 2: Go to Docker Engine
echo   - Click "Docker Engine" in left sidebar
echo.
echo STEP 3: Add DNS Configuration
echo   - Find the JSON configuration
echo   - Add this line after the first opening brace:
echo.
echo   "dns": ["8.8.8.8", "8.8.4.4"],
echo.
echo   Example:
echo   {
echo     "dns": ["8.8.8.8", "8.8.4.4"],
echo     "builder": {
echo       ...
echo     }
echo   }
echo.
echo STEP 4: Apply and Restart
echo   - Click "Apply & Restart"
echo   - Wait 30 seconds
echo.
echo STEP 5: Test the Fix
echo   - Run: docker pull hello-world
echo.
echo STEP 6: Build Images
echo   - Run: build-images.bat
echo.
echo ============================================
echo Press any key to open Docker Desktop Settings...
pause > nul
start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
