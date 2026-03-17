# PDF to Speech Converter

Convert PDFs to high-quality audio with a modern web UI and powerful REST API. Supports multiple TTS engines, batch processing, and async job management.

## ✨ Features

### 🖥️ Modern Web UI
- Drag-and-drop PDF upload
- Real-time TTS engine & voice selection
- Speed control (0.5x - 2.0x)
- Batch file processing
- Live job status tracking
- One-click audio download

### 🔌 REST API
- Single & batch file conversion endpoints
- Async job queue for large PDFs
- Voice listing by engine
- Job status polling
- Direct audio file downloads
- JSON responses for easy integration

### ⚙️ Multiple TTS Engines
- **Google TTS** - Online, high quality, 15+ languages
- **System TTS** - Offline, fast, Windows/macOS/Linux compatible
- **Pluggable architecture** - Ready for ElevenLabs, Coqui, etc.

### 📄 PDF Processing
- Text extraction with PyMuPDF
- OCR fallback for scanned documents (Tesseract)
- Page-by-page extraction
- Metadata extraction (title, author, page count)

### 🎵 Audio Processing
- Speed adjustment (0.5x - 2.0x)
- Volume normalization
- Multiple output formats (MP3, WAV, M4B)
- Chapter splitting support
- Audio metadata retrieval

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- FFmpeg (audio processing)
- Tesseract OCR (for scanned PDFs)

### Installation

```bash
# Clone and navigate
git clone https://github.com/emsilver987/Free_PDF_To_Speech.git
cd Free_PDF_To_Speech

# Run one-time setup (installs dependencies, creates directories)
chmod +x SETUP.sh
./SETUP.sh
```

The setup script will:
- ✅ Create a Python virtual environment
- ✅ Install all dependencies
- ✅ Create runtime directories (uploads/, outputs/, jobs/)
- ✅ Check for system dependencies (ffmpeg, tesseract)
- ✅ Show startup instructions

### Starting the Application

The application needs **TWO terminals** running simultaneously.

**Option 1: Using the provided startup scripts**

Terminal 1 (Backend API):
```bash
./start.sh
# Runs on http://localhost:5000
```

Terminal 2 (Frontend Web UI):
```bash
./start-frontend.sh
# Runs on http://localhost:8080
```

**Option 2: Manual startup**

Terminal 1 (Backend API):
```bash
source venv/bin/activate
python run.py
# API runs on http://localhost:5000
```

Terminal 2 (Frontend):
```bash
source venv/bin/activate
python -m http.server 8080 --directory frontend
# UI runs on http://localhost:8080
```

Then **open your browser to:** `http://localhost:8080`

### Troubleshooting Startup

**"API Unavailable" error in UI?**
- Make sure backend is running: `python run.py` in Terminal 1
- Check that http://localhost:5000/api/health returns a response
- Both terminals must be active simultaneously

**"Permission denied" on SETUP.sh?**
```bash
chmod +x SETUP.sh
./SETUP.sh
```

**Windows users:**
```bash
# Create venv
python -m venv venv
venv\Scripts\Activate

# Install dependencies
pip install -r requirements.txt

# Start backend
python run.py

# In another terminal:
python -m http.server 8080 --directory frontend
```

---

## 📖 Usage

### Web UI

1. **Upload PDFs**: Drag files into the drop zone or click to browse
2. **Configure**: Select TTS engine, voice, and playback speed
3. **Process**: Click "Convert" to start processing
4. **Monitor**: Check the Jobs tab for real-time status
5. **Download**: Get your audio file when ready

### REST API

See [API.md](./API.md) for complete endpoint documentation.

#### Convert a Single PDF
```bash
curl -X POST http://localhost:5000/api/convert \
  -F "file=@document.pdf" \
  -F "engine=gtts" \
  -F "voice=en" \
  -F "speed=1.2" \
  -F "async=true"
```

#### Batch Processing
```bash
curl -X POST http://localhost:5000/api/batch \
  -F "files=@doc1.pdf" \
  -F "files=@doc2.pdf" \
  -F "engine=gtts" \
  -F "speed=1.0"
```

#### Check Job Status
```bash
curl http://localhost:5000/api/jobs/{job_id}
```

---

## 📁 Project Structure

```
.
├── backend/                          # Flask API server
│   ├── app.py                       # Main API application
│   ├── converters/
│   │   ├── pdf_processor.py        # PDF extraction + OCR
│   │   ├── tts_engine.py           # TTS abstraction layer
│   │   └── audio_processor.py      # Speed, volume, format conversion
│   └── tasks/
│       └── job_queue.py            # Async job processing
├── frontend/
│   └── index.html                  # Modern web UI (no build required)
├── examples/                        # Integration examples & scripts
├── legacy/                          # Original simple scripts
├── uploads/                         # Temporary PDF uploads
├── outputs/                         # Generated audio files
├── jobs/                            # Job metadata & history
├── requirements.txt                # Python dependencies
├── SETUP.sh                        # Quick setup script
├── API.md                          # REST API documentation
└── README.md                       # This file
```

---

## 🔧 Configuration

### Environment Variables

```bash
export FLASK_ENV=production
export FLASK_HOST=0.0.0.0
export FLASK_PORT=5000
export MAX_FILE_SIZE=100  # MB
```

### TTS Engine Configuration

**Google TTS** (default):
- Requires internet connection
- Best for high-quality audio
- Supports 15+ languages
- No API key needed

**System TTS** (offline):
- No internet required
- Faster processing
- Good for quick conversions
- Windows/macOS/Linux compatible

---

## 🐛 Troubleshooting

### Module Import Errors
```bash
# Ensure virtual environment is activated
source venv/bin/activate
# Reinstall dependencies
pip install -r requirements.txt
```

### "Couldn't find ffmpeg"
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Windows: Download from https://ffmpeg.org/download.html
```

### "Tesseract not found" (OCR)
```bash
# macOS
brew install tesseract

# Ubuntu/Debian
sudo apt install tesseract-ocr

# Windows: https://github.com/UB-Mannheim/tesseract/wiki
```

### API Returns 500 Errors
```bash
# Run in debug mode for detailed logs
python backend/app.py --debug
```

### Slow Conversion
- Use `system` TTS for offline mode
- Set speed to 1.2-1.5x
- Use async mode for files >10MB

---

## 📚 Documentation

- **[API.md](./API.md)** - Complete REST API reference
- **[examples/](./examples/)** - Integration examples & scripts
- **[legacy/](./legacy/)** - Original simple CLI scripts

---

## 🛣️ Roadmap

### Completed ✅
- Web UI with drag-and-drop upload
- REST API with async job queue
- Multiple TTS engines
- Audio post-processing
- Batch file conversion

### Coming Soon 🔜
- [ ] ElevenLabs TTS integration (ultra-high quality voices)
- [ ] Coqui TTS support (open-source neural voices)
- [ ] Cloud storage integration (AWS S3, Google Drive)
- [ ] Podcast platform publishing
- [ ] Advanced text preprocessing & cleanup
- [ ] Conversation history & analytics
- [ ] Docker containerization
- [ ] Webhook notifications
- [ ] Authentication & multi-user support
- [ ] Chapter management & metadata

---

## 💡 Examples

### Python Integration
```python
import requests

# Single file conversion
response = requests.post(
    "http://localhost:5000/api/convert",
    files={"file": open("document.pdf", "rb")},
    data={
        "engine": "gtts",
        "voice": "en",
        "speed": 1.2,
        "async": True
    }
)

job_id = response.json()["job_id"]
print(f"Job queued: {job_id}")
```

### JavaScript Integration
```javascript
const formData = new FormData();
formData.append("file", pdfFile);
formData.append("engine", "gtts");
formData.append("speed", 1.2);
formData.append("async", true);

const response = await fetch("http://localhost:5000/api/convert", {
  method: "POST",
  body: formData
});

const job = await response.json();
console.log(`Job ID: ${job.job_id}`);
```

---

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

---

## 📄 License

MIT License - See [LICENSE](./LICENSE) file

---

## 🙏 Credits

Built on top of:
- [PyMuPDF](https://pymupdf.readthedocs.io/) - PDF processing
- [gTTS](https://gtts.readthedocs.io/) - Google Text-to-Speech
- [pyttsx3](https://pyttsx3.readthedocs.io/) - Offline TTS
- [pydub](https://github.com/jiaaro/pydub) - Audio processing
- [pytesseract](https://github.com/madmaze/pytesseract) - OCR

---

## 📞 Support

- **Issues**: Open a GitHub issue for bugs or features
- **Discussions**: Check discussions for questions
- **Docs**: See [API.md](./API.md) for detailed endpoint docs
