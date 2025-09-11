# PDF Text-to-Speech Converter

A Python application that converts PDF documents to audio using text-to-speech technology. Supports both online (Google TTS) and offline (Windows TTS) modes.

## Features

- 📄 **PDF Processing**: Extract text from PDF files using PyMuPDF
- 🔍 **OCR Support**: Automatic OCR fallback for scanned PDFs using Tesseract
- 🎵 **Multiple TTS Options**: 
  - Google Text-to-Speech (online, high quality)
  - Windows built-in TTS (offline, no internet required)
- ⚡ **Audio Processing**: Speed up audio playback (1.5x speed)
- 🎯 **Easy Setup**: One-command environment setup

## Prerequisites

- Python 3.8 or higher
- Windows OS (for offline TTS)
- Internet connection (for Google TTS only)

## Quick Start

### 1. Clone or Download
```bash
git clone <repository-url>
cd tts
```

### 2. Set Up Environment
```bash
# Option A: Use the batch file (Windows)
activate.bat

# Option B: Manual activation
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
# Online TTS (requires internet)
python tts.py

# Offline TTS (no internet required)
python tts_offline.py

# Test environment
python test_env.py
```

## Usage

### Basic Usage

1. **Place your PDF file** in the `tts` directory
2. **Update the PDF filename** in the script:
   ```python
   pdf_path = "your-document.pdf"
   ```
3. **Run the appropriate script**:
   - `python tts.py` - For Google TTS (better quality, requires internet)
   - `python tts_offline.py` - For Windows TTS (offline, faster)

### Output

- **Audio file**: `your-document.mp3` (same name as PDF)
- **Temporary files**: Automatically cleaned up

## Scripts Overview

| Script | Description | Internet Required |
|--------|-------------|-------------------|
| `tts.py` | Google TTS with audio processing | ✅ Yes |
| `tts_offline.py` | Windows built-in TTS | ❌ No |
| `test_env.py` | Test all dependencies | ❌ No |

## Dependencies

- **PyMuPDF**: PDF text extraction
- **Pillow**: Image processing for OCR
- **pytesseract**: Optical Character Recognition
- **gTTS**: Google Text-to-Speech
- **pydub**: Audio processing and manipulation
- **pyttsx3**: Offline text-to-speech
- **audioop-lts**: Python 3.13 compatibility

## Troubleshooting

### Common Issues

1. **"ModuleNotFoundError"**
   ```bash
   # Make sure virtual environment is activated
   .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2. **"Couldn't find ffmpeg"**
   - This is a warning, not an error
   - The script will still work for basic audio processing

3. **Google TTS Connection Issues**
   - Check internet connection
   - Use `tts_offline.py` as alternative

4. **OCR Not Working**
   - Ensure Tesseract is installed on your system
   - For Windows: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

### Testing Environment

Run the test script to verify everything is working:
```bash
python test_env.py
```

Expected output:
```
Testing TTS environment...
========================================
✅ PyMuPDF (fitz) imported successfully
✅ Pillow (PIL) imported successfully
✅ pytesseract imported successfully
✅ gTTS imported successfully
✅ pydub imported successfully
✅ pyttsx3 imported successfully
✅ PDF opened successfully: X pages
🎉 All tests passed! Environment is ready.
```

## File Structure

```
tts/
├── .venv/                 # Virtual environment
├── .gitignore            # Git ignore rules
├── README.md             # This file
├── requirements.txt      # Python dependencies
├── activate.bat          # Easy activation script
├── tts.py               # Main script (Google TTS)
├── tts_offline.py       # Offline TTS script
├── test_env.py          # Environment test script
└── your-document.pdf    # Your PDF files (ignored by git)
```

## Customization

### Audio Settings (tts_offline.py)
```python
engine.setProperty('rate', 200)      # Speech speed
engine.setProperty('volume', 0.9)    # Volume (0.0 to 1.0)
```

### Audio Speed (tts.py)
```python
# Change speed multiplier (1.5 = 1.5x faster)
faster = sound._spawn(
    sound.raw_data,
    overrides={"frame_rate": int(sound.frame_rate * 1.5)}
).set_frame_rate(sound.frame_rate)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

If you encounter any issues:
1. Check the troubleshooting section
2. Run `python test_env.py` to diagnose problems
3. Create an issue with error details and system information
