#!/bin/bash

# Quick start script for development
# This starts ONLY the backend API
# Frontend needs to be run in a separate terminal

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Activate venv
source venv/bin/activate

# Start backend
echo "🎵 Starting PDF-to-Speech Backend API..."
echo "📡 Running on http://localhost:5000"
echo ""
echo "Frontend should be running separately on http://localhost:8080"
echo "Start frontend in another terminal with:"
echo "  cd $SCRIPT_DIR && source venv/bin/activate && python -m http.server 8080 --directory frontend"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python run.py
