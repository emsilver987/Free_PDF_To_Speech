"""
PDF-to-Speech REST API
Handles PDF conversion with configurable TTS engines and audio processing
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import uuid
from pathlib import Path
import json
from datetime import datetime
import logging

# Import conversion modules
import sys
from pathlib import Path

# Add backend directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from converters.pdf_processor import PDFProcessor
from converters.tts_engine import TTSEngine
from converters.audio_processor import AudioProcessor
from tasks.job_queue import JobQueue

# Setup
app = Flask(__name__)
CORS(app)
logger = logging.getLogger(__name__)

# Config
UPLOAD_FOLDER = Path("uploads")
OUTPUT_FOLDER = Path("outputs")
JOBS_FOLDER = Path("jobs")
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
ALLOWED_EXTENSIONS = {"pdf"}

for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER, JOBS_FOLDER]:
    folder.mkdir(exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE

# Initialize job queue
job_queue = JobQueue(JOBS_FOLDER)


@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint"""
    import shutil
    
    ffmpeg_available = shutil.which('ffmpeg') is not None and shutil.which('ffprobe') is not None
    tesseract_available = shutil.which('tesseract') is not None
    
    warnings = []
    if not ffmpeg_available:
        warnings.append("ffmpeg not installed - speed adjustment disabled")
    if not tesseract_available:
        warnings.append("tesseract not installed - OCR for scanned PDFs disabled")
    
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "features": {
            "ffmpeg": ffmpeg_available,
            "tesseract": tesseract_available
        },
        "warnings": warnings if warnings else None
    })


@app.route("/api/voices", methods=["GET"])
def list_voices():
    """Get available voices for all TTS engines"""
    engine_type = request.args.get("engine", "gtts")  # gtts, elevenlabs, coqui, system
    
    try:
        tts = TTSEngine()
        voices = tts.get_voices(engine_type)
        return jsonify({
            "engine": engine_type,
            "voices": voices
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/convert", methods=["POST"])
def convert_pdf():
    """
    Main conversion endpoint
    
    Form data:
    - file: PDF file (required)
    - engine: TTS engine (gtts, elevenlabs, coqui, system) - default: gtts
    - voice: Voice ID - optional
    - speed: Speech speed 0.5-2.0 - default: 1.0
    - async: Run asynchronously - default: false
    """
    
    # Validate file
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files["file"]
    if file.filename == "" or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type (must be PDF)"}), 400
    
    # Parse parameters
    engine = request.form.get("engine", "gtts")
    voice = request.form.get("voice")
    speed = float(request.form.get("speed", 1.0))
    async_mode = request.form.get("async", "false").lower() == "true"
    
    # Validate parameters
    if not (0.5 <= speed <= 2.0):
        return jsonify({"error": "Speed must be between 0.5 and 2.0"}), 400
    
    # Save uploaded file
    filename = secure_filename(file.filename)
    job_id = str(uuid.uuid4())
    file_path = UPLOAD_FOLDER / filename
    file.save(file_path)
    
    # Create job metadata
    job_data = {
        "job_id": job_id,
        "filename": filename,
        "file_path": str(file_path),
        "engine": engine,
        "voice": voice,
        "speed": speed,
        "status": "queued",
        "created_at": datetime.now().isoformat(),
        "started_at": None,
        "completed_at": None,
        "output_file": None,
        "error": None
    }
    
    if async_mode:
        # Queue for async processing
        job_queue.enqueue(job_data)
        return jsonify({
            "job_id": job_id,
            "status": "queued",
            "message": "Conversion queued. Check status with /api/jobs/{job_id}"
        }), 202
    else:
        # Synchronous processing
        try:
            output_path = process_conversion(job_data)
            job_data["status"] = "completed"
            job_data["completed_at"] = datetime.now().isoformat()
            job_data["output_file"] = str(output_path)
            
            return jsonify({
                "job_id": job_id,
                "status": "completed",
                "output_file": str(output_path),
                "download_url": f"/api/download/{job_id}"
            }), 200
        except Exception as e:
            job_data["status"] = "failed"
            job_data["error"] = str(e)
            logger.error(f"Conversion failed for job {job_id}: {str(e)}")
            return jsonify({"error": str(e)}), 500


@app.route("/api/batch", methods=["POST"])
def batch_convert():
    """
    Batch conversion endpoint
    
    JSON body:
    {
        "files": [list of file upload objects],
        "engine": "gtts",
        "voice": "optional",
        "speed": 1.0
    }
    """
    
    if "files" not in request.files:
        return jsonify({"error": "No files provided"}), 400
    
    files = request.files.getlist("files")
    if not files:
        return jsonify({"error": "No files provided"}), 400
    
    engine = request.form.get("engine", "gtts")
    voice = request.form.get("voice")
    speed = float(request.form.get("speed", 1.0))
    
    job_ids = []
    
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            job_id = str(uuid.uuid4())
            file_path = UPLOAD_FOLDER / filename
            file.save(file_path)
            
            job_data = {
                "job_id": job_id,
                "filename": filename,
                "file_path": str(file_path),
                "engine": engine,
                "voice": voice,
                "speed": speed,
                "status": "queued",
                "created_at": datetime.now().isoformat(),
                "started_at": None,
                "completed_at": None,
                "output_file": None,
                "error": None
            }
            
            job_queue.enqueue(job_data)
            job_ids.append(job_id)
    
    return jsonify({
        "job_count": len(job_ids),
        "job_ids": job_ids,
        "message": "All files queued for batch processing"
    }), 202


@app.route("/api/jobs/<job_id>", methods=["GET"])
def get_job_status(job_id):
    """Get status of a conversion job"""
    try:
        job_data = job_queue.get_job(job_id)
        return jsonify(job_data), 200
    except KeyError:
        return jsonify({"error": "Job not found"}), 404


@app.route("/api/download/<job_id>", methods=["GET"])
def download_file(job_id):
    """Download converted audio file"""
    try:
        job_data = job_queue.get_job(job_id)
        
        if job_data["status"] != "completed":
            return jsonify({"error": "Conversion not completed"}), 400
        
        output_path = Path(job_data["output_file"])
        if not output_path.exists():
            return jsonify({"error": "File not found"}), 404
        
        return send_file(output_path, as_attachment=True, download_name=output_path.name)
    except KeyError:
        return jsonify({"error": "Job not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def process_conversion(job_data):
    """Execute the PDF-to-speech conversion"""
    job_data["status"] = "processing"
    job_data["started_at"] = datetime.now().isoformat()
    
    try:
        # Step 1: Extract text from PDF
        pdf_processor = PDFProcessor()
        text = pdf_processor.extract_text(job_data["file_path"])
        
        # Step 2: Generate speech
        tts = TTSEngine()
        audio_path = tts.synthesize(
            text,
            engine=job_data["engine"],
            voice=job_data["voice"],
            output_dir=OUTPUT_FOLDER
        )
        
        # Step 3: Process audio
        audio_processor = AudioProcessor()
        final_path = audio_processor.process_audio(
            audio_path,
            speed=job_data["speed"]
        )
        
        return final_path
    except Exception as e:
        job_data["status"] = "failed"
        job_data["error"] = str(e)
        raise


def allowed_file(filename):
    """Check if file is allowed"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
