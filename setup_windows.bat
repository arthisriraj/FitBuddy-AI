@echo off
title FitBuddy Setup
echo ============================================
echo             FitBuddy Setup
echo ============================================
python --version
if errorlevel 1 (
    echo Python was not found in PATH.
    echo Install Python and try again.
    pause
    exit /b 1
)
python -m venv venv
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
if not exist ".env" copy ".env.example" ".env"
echo.
echo Setup complete.
echo Edit .env and add GOOGLE_API_KEY.
echo Then run: run_windows.bat
pause
