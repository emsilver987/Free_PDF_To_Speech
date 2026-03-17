#!/bin/bash

# PDF-to-Speech Enhanced Setup Script
# This script sets up the environment and optionally starts the application

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "🎵 PDF-to-Speech Enhanced - Setup & Run"
echo "========================================"
echo ""

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found${NC}"
    echo "   Please install Python 3.8 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✅ Python${NC} $PYTHON_VERSION"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${BLUE}📦 Creating virtual environment...${NC}"
    python3 -m venv venv
else
    echo -e "${GREEN}✅ Virtual environment${NC} already exists"
fi

# Activate virtual environment
echo -e "${BLUE}🔄 Activating virtual environment...${NC}"
source venv/bin/activate

# Install/upgrade dependencies
echo -e "${BLUE}📚 Installing Python dependencies...${NC}"
pip install -q -r requirements.txt

# Create runtime directories
echo -e "${BLUE}📁 Creating runtime directories...${NC}"
mkdir -p uploads outputs jobs

echo ""
echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""

# Check system dependencies
echo -e "${BLUE}🔍 Checking system dependencies...${NC}"
FFMPEG_OK=false
TESSERACT_OK=false

if command -v ffmpeg &> /dev/null; then
    echo -e "${GREEN}✅ ffmpeg${NC} found"
    FFMPEG_OK=true
else
    echo -e "${YELLOW}⚠️  ffmpeg${NC} not found (required for audio processing)"
    echo "   Install: brew install ffmpeg (macOS) or sudo apt install ffmpeg (Ubuntu)"
fi

if command -v tesseract &> /dev/null; then
    echo -e "${GREEN}✅ tesseract${NC} found"
    TESSERACT_OK=true
else
    echo -e "${YELLOW}⚠️  tesseract${NC} not found (only needed for scanned PDFs)"
    echo "   Install: brew install tesseract (macOS) or sudo apt install tesseract-ocr (Ubuntu)"
fi

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "🚀 Ready to start the application!"
echo ""
echo "The application needs TWO terminals running simultaneously:"
echo ""
echo -e "${BLUE}Terminal 1 - Backend API:${NC}"
echo "  python run.py"
echo "  (API will run on http://localhost:5000)"
echo ""
echo -e "${BLUE}Terminal 2 - Frontend Web UI:${NC}"
echo "  python -m http.server 8080 --directory frontend"
echo "  (UI will run on http://localhost:8080)"
echo ""
echo "Then open your browser to: ${BLUE}http://localhost:8080${NC}"
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Ask if user wants to start services
read -p "Start both services now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "⚠️  This script can only start one service (backend)"
    echo "Please open a second terminal and run:"
    echo "  cd $SCRIPT_DIR"
    echo "  source venv/bin/activate"
    echo "  python -m http.server 8080 --directory frontend"
    echo ""
    echo "Starting backend API..."
    echo ""
    echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
    python run.py
else
    echo ""
    echo "Run this command in another terminal to start the frontend:"
    echo "  cd $SCRIPT_DIR && source venv/bin/activate && python -m http.server 8080 --directory frontend"
    echo ""
fi
