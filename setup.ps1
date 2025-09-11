# PDF Text-to-Speech Setup Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    PDF Text-to-Speech Setup Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from https://python.org" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
python -m venv .venv

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".venv\Scripts\Activate.ps1"

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
python -m pip install --upgrade pip
pip install -r requirements.txt

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "           Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "To use the TTS converter:" -ForegroundColor Cyan
Write-Host "1. Run: .venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "2. Place your PDF in this folder" -ForegroundColor White
Write-Host "3. Run: python tts.py (online) or python tts_offline.py (offline)" -ForegroundColor White
Write-Host ""
Write-Host "To test the setup: python test_env.py" -ForegroundColor Cyan
Write-Host ""
Read-Host "Press Enter to continue"
