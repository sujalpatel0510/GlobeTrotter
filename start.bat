@echo off
echo ========================================================
echo   Starting GlobeTrotter Travel Planning Platform
echo   Powered by Flask and PostgreSQL
echo ========================================================
echo.
cd /d "%~dp0"

echo [1/2] Initializing PostgreSQL database tables...
.venv\Scripts\python.exe run.py --init-db

echo.
echo [2/2] Starting Flask Web Server on http://localhost:5000 ...
echo Press Ctrl+C to stop the server.
echo.
start http://localhost:5000
.venv\Scripts\python.exe run.py
pause
