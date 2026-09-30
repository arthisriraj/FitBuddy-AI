@echo off
title FitBuddy
echo ============================================
echo        FitBuddy - AI Fitness Plan Generator
echo ============================================
if not exist "venv\Scripts\activate.bat" (
    echo Virtual environment not found.
    echo Run setup first:
    echo python -m venv venv
    echo venv\Scripts\activate
    echo pip install -r requirements.txt
    pause
    exit /b 1
)
call venv\Scripts\activate.bat
uvicorn app.main:app --reload
pause
