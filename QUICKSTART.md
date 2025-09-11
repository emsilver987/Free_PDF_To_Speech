# Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1. Setup Environment
```bash
# Windows (Command Prompt)
setup.bat

# Windows (PowerShell)
.\setup.ps1

# Manual setup
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Add Your PDF
- Place your PDF file in the `tts` folder
- Update the filename in the script:
  ```python
  pdf_path = "your-document.pdf"  # Change this line
  ```

### 3. Run TTS
```bash
# Online (Google TTS - better quality)
python tts.py

# Offline (Windows TTS - no internet needed)
python tts_offline.py
```

## 📁 What You'll Get
- `your-document.mp3` - Audio file ready to play!

## 🔧 Troubleshooting
```bash
# Test if everything works
python test_env.py

# If you see all ✅ marks, you're good to go!
```

## 📋 File Checklist
- [ ] Python 3.8+ installed
- [ ] PDF file in tts folder
- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] Script filename updated

That's it! 🎉
