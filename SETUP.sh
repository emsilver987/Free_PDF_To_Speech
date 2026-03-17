#!/bin/bash

# Setup script for PDF-to-Speech Enhanced

echo "🎵 PDF to Speech - Setup"
echo "================================"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

echo "✅ Python version: $(python3 --version)"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt --quiet

# Create directories
echo "📁 Creating directories..."
mkdir -p uploads outputs jobs

# Check system dependencies
echo ""
echo "🔍 Checking system dependencies..."

if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  ffmpeg not found (required for audio processing)"
    echo "   macOS: brew install ffmpeg"
    echo "   Ubuntu: sudo apt install ffmpeg"
fi

if ! command -v tesseract &> /dev/null; then
    echo "⚠️  tesseract not found (required for OCR)"
    echo "   macOS: brew install tesseract"
    echo "   Ubuntu: sudo apt install tesseract-ocr"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 To start:"
echo "   1. Backend: python backend/app.py"
echo "   2. Frontend: python -m http.server 8080 --directory frontend"
echo "   3. Open: http://localhost:8080"
