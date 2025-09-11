@echo off
echo ========================================
echo    PDF Text-to-Speech Setup Script
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo Python found! Creating virtual environment...
python -m venv .venv

echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ========================================
echo           Setup Complete!
echo ========================================
echo.
echo To use the TTS converter:
echo 1. Run: activate.bat
echo 2. Place your PDF in this folder
echo 3. Run: python tts.py (online) or python tts_offline.py (offline)
echo.
echo To test the setup: python test_env.py
echo.
pause
