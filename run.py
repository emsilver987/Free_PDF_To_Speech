#!/usr/bin/env python3
"""
Entry point for PDF-to-Speech API server

Usage: python run.py [--host HOST] [--port PORT] [--debug]
"""

import sys
import argparse
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from app import app


def main():
    parser = argparse.ArgumentParser(description="PDF-to-Speech API Server")
    parser.add_argument("--host", default="0.0.0.0", help="Server host (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=5000, help="Server port (default: 5000)")
    parser.add_argument("--debug", action="store_true", help="Run in debug mode")
    
    args = parser.parse_args()
    
    print(f"🎵 PDF-to-Speech API Server")
    print(f"📡 Starting on {args.host}:{args.port}")
    if args.debug:
        print(f"🐛 Debug mode enabled")
    print()
    
    app.run(debug=args.debug, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
