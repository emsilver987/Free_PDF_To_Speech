#!/bin/bash

# Start only the frontend web server
# Backend should be running separately on port 5000

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Activate venv (optional, but good practice)
if [ -d "venv" ]; then
    source venv/bin/activate
fi

echo "🎵 Starting PDF-to-Speech Frontend..."
echo "🌐 UI will be available at http://localhost:8080"
echo ""
echo "Backend should be running separately on http://localhost:5000"
echo "Start backend in another terminal with:"
echo "  cd $SCRIPT_DIR && source venv/bin/activate && python run.py"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

cd frontend && python -m http.server 8080
