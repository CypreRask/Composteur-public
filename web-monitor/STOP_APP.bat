@echo off
echo ==========================================
echo  NETTOYAGE D'URGENCE - COMPOSTEUR
echo ==========================================
echo.

echo [1/3] Fermeture de la fenetre "Backend"...
taskkill /FI "WINDOWTITLE eq Backend" /T /F >nul 2>&1

echo [2/3] Liberation du port 8085 (API)...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8085" ^| find "LISTENING"') do (
    echo     - Tuer le processus PID: %%a
    taskkill /PID %%a /F >nul 2>&1
)

echo [3/3] Liberation du port 9999 (Frontend)...
for /f "tokens=5" %%a in ('netstat -aon ^| find ":9999" ^| find "LISTENING"') do (
    echo     - Tuer le processus PID: %%a
    taskkill /PID %%a /F >nul 2>&1
)

echo.
echo [OK] Tout est propre. Tu peux relancer RUN_ALL.bat.
timeout /t 3 >nul
