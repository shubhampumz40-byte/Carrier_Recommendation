@echo off
echo Starting Career Compass Server...
echo.

REM Start Flask server in background
echo [1/2] Starting Flask application...
start /B python run.py

REM Wait a moment for Flask to start
timeout /t 5 /nobreak >nul

REM Start Cloudflare tunnel
echo [2/2] Starting Cloudflare tunnel...
echo.
echo Your Career Compass will be available at:
echo - Local: http://localhost:5000
echo - Network: http://192.168.0.115:5000
echo.
echo Starting public tunnel...
.\cloudflared.exe tunnel --url http://localhost:5000

echo.
echo Press Ctrl+C to stop the server
pause