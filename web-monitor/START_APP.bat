@echo off
setlocal enabledelayedexpansion
title SmartCompost - Auto Launcher

echo ==============================================
echo      SMART COMPOST - DEMARRAGE AUTO
echo ==============================================

cd /d "%~dp0"

echo.
echo [1/3] VERIFICATION BACKEND (Python)
echo -----------------------------------
if not exist "backend\venv" (
    echo     Warning: Venv introuvable. Creation en cours...
    python -m venv backend\venv
) else (
    echo     Venv detecte.
)

echo     Activation et installation des dependances...
call backend\venv\Scripts\activate
pip install -r backend\requirements.txt

echo.
echo [1.5/3] VERIFICATION MODELE IA
echo -----------------------------------
if not exist "backend\ml\compost_model.pkl" (
    echo     Modele IA introuvable. Entrainement initial...
    cd backend
    python ml/train.py
    cd ..
) else (
    echo     Modele IA present.
)

echo.
echo [2/3] VERIFICATION FRONTEND (Node.js)
echo -----------------------------------
cd frontend
echo     Installation/Mise a jour des paquets npm...
call npm install
cd ..

echo.
echo [3/3] LANCEMENT DES SERVICES
echo -----------------------------------

:: START BACKEND
:: On lance uvicorn directement pour eviter les dependances cachees
start "SmartCompost Backend API" cmd /k "cd backend && venv\Scripts\activate && python start_service.py"

:: START FRONTEND
start "SmartCompost Monitor UI" cmd /k "cd frontend && npm run dev"

echo.
echo ==============================================
echo    Tout est lance ! 
echo    Backend : http://localhost:8085
echo    Frontend: http://localhost:9999
echo ==============================================
echo.
echo Tu peux fermer cette fenetre, les serveurs tournent en arriere-plan.
pause
