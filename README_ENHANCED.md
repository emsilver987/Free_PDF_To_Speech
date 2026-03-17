# PDF to Speech - Enhanced Edition

Convert PDFs to high-quality audio with a modern web UI and powerful REST API.

## What's New

### 🖥️ Web UI
- Drag-and-drop PDF upload
- Real-time TTS engine & voice selection
- Speed control (0.5x - 2.0x)
- Batch processing support
- Job status tracking with live updates
- One-click audio download

### 🔌 REST API
- Single & batch file conversion endpoints
- Async job queue for large PDFs
- Voice listing by engine
- Job status polling
- Direct audio file downloads
- JSON responses for easy integration

### ⚙️ Multiple TTS Engines
- **Google TTS** (online, high quality, multiple languages)
- **System TTS** (offline, fast, Windows/macOS/Linux)
- Pluggable architecture for ElevenLabs, Coqui (coming soon)

### 🎵 Audio Processing
- Speed adjustment (0.5x - 2.0x)
- Volume normalization
- Chapter splitting support
- Multiple output formats (MP3, WAV, M4B)

---

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

**System Requirements:**
- Python 3.8+
- FFmpeg (for audio processing)
- Tesseract OCR (for scanned PDFs)

### 2. Start the Backend API

```bash
python backend/app.py
```

API runs on `http://localhost:5000`

### 3. Open the Web UI

```bash
# Option A: Serve with Python
python -m http.server 8080 --directory frontend

# Option B: Open directly
open frontend/index.html
```

UI runs on `http://localhost:8080`

---

## Usage

### Via Web UI

1. **Upload**: Drag PDFs into the upload zone or click to browse
2. **Configure**: Select TTS engine, voice, and speed
3. **Convert**: Click "Convert" to process
4. **Download**: Check the Jobs tab for status and download when ready

### Via REST API

See [API.md](./API.md) for complete endpoint documentation.

#### Example: Convert a Single PDF

```bash
curl -X POST http://localhost:5000/api/convert \
  -F "file=@document.pdf" \
  -F "engine=gtts" \
  -F "voice=en" \
  -F "speed=1.2" \
  -F "async=true"
```

#### Example: Batch Processing

```bash
curl -X POST http://localhost:5000/api/batch \
  -F "files=@doc1.pdf" \
  -F "files=@doc2.pdf" \
  -F "engine=gtts" \
  -F "speed=1.0"
```

---

## Project Structure

```
pdf-to-speech-enhanced/
├── backend/
│   ├── app.py                    # Flask API server
│   ├── converters/
│   │   ├── pdf_processor.py     # PDF text extraction + OCR
│   │   ├── tts_engine.py        # TTS abstraction (Google, System, etc)
│   │   └── audio_processor.py   # Speed, volume, format conversion
│   └── tasks/
│       └── job_queue.py         # Async job processing
├── frontend/
│   └── index.html               # Modern single-page web UI
├── uploads/                     # Uploaded PDFs (temporary)
├── outputs/                     # Generated audio files
├── jobs/                        # Job metadata & history
├── requirements.txt
├── API.md                       # REST API documentation
└── README_ENHANCED.md           # This file
```

---

## Features

### PDF Processing
- ✅ Text extraction (PyMuPDF)
- ✅ OCR fallback for scanned documents (Tesseract)
- ✅ Page-by-page extraction
- ✅ Metadata extraction (title, author, page count)

### Text-to-Speech
- ✅ Google TTS (multiple languages, high quality)
- ✅ System TTS (offline, Windows/macOS/Linux)
- ✅ Voice selection by engine
- ✅ Multiple language support

### Audio Processing
- ✅ Speed adjustment (0.5x - 2.0x)
- ✅ Volume normalization
- ✅ Format conversion (MP3, WAV, M4B)
- ✅ Chapter splitting
- ✅ Audio metadata retrieval

### Job Management
- ✅ Async processing queue
- ✅ Job status tracking
- ✅ Batch file processing
- ✅ Job history persistence
- ✅ Error reporting

### Integration
- ✅ REST API for all features
- ✅ CORS enabled for cross-origin requests
- ✅ JSON responses
- ✅ Async/await support
- ✅ Webhook ready (extensible)

---

## Configuration

### Environment Variables

```bash
export FLASK_ENV=production
export FLASK_HOST=0.0.0.0
export FLASK_PORT=5000
export MAX_FILE_SIZE=100  # MB
```

### Customization

**Change default TTS engine:**
```python
# In backend/app.py
DEFAULT_ENGINE = "system"  # or "gtts"
```

**Adjust speech speed defaults:**
```python
# In backend/converters/tts_engine.py
engine.setProperty('rate', 150)  # Words per minute
```

---

## Troubleshooting

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "Couldn't find ffmpeg"
```bash
# macOS
brew install ffmpeg

# Ubuntu
sudo apt install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

### "Tesseract not found"
```bash
# macOS
brew install tesseract

# Ubuntu
sudo apt install tesseract-ocr

# Windows
# Download from https://github.com/UB-Mannheim/tesseract/wiki
# Set environment variable TESSERACT_PATH
```

### API returns 500 errors
Check Flask logs for detailed error messages:
```bash
python backend/app.py --debug
```

### Slow conversion speed
- Use `system` TTS instead of `gtts` for offline mode
- Increase speed parameter (1.2-1.5x is comfortable)
- For very large PDFs (>50MB), use async mode

---

## Next Steps & Roadmap

### Implemented (Ideas 1 & 6)
- ✅ Modern web UI with drag-and-drop
- ✅ Full REST API with async support

### Coming Soon
- [ ] ElevenLabs TTS integration (high-quality voices)
- [ ] Coqui TTS support (open-source neural voices)
- [ ] Cloud storage integration (AWS S3, Google Drive)
- [ ] Podcast platform publishing
- [ ] Advanced text cleanup & preprocessing
- [ ] Analytics & conversion history
- [ ] Docker containerization
- [ ] Webhooks for job completion
- [ ] Authentication & multi-user support

---

## Contributing

This is an open-source project. Ideas, PRs, and bug reports are welcome!

---

## License

MIT License - See original [Free_PDF_To_Speech](https://github.com/emsilver987/Free_PDF_To_Speech) repo.

---

## Support

- **API Issues**: Check [API.md](./API.md)
- **UI Issues**: Open browser console (F12) for errors
- **General Help**: See troubleshooting section above
