@echo off
chcp 65001 >nul
echo ==========================================
echo  COMPOST MONITOR - Lancement Complet
echo ==========================================
echo.

cd /d "%~dp0"
echo [INFO] Repertoire: %CD%
echo.

echo [1/2] Lancement Backend (port 8085)...
start "Backend" cmd /k "cd backend && python start_service.py"

echo [WAIT] Attente 4 secondes...
timeout /t 4 >nul

echo [2/2] Lancement Frontend (port 9999)...
cd frontend
npm run dev

taskkill /FI "WINDOWTITLE eq Backend" >nul 2>&1
