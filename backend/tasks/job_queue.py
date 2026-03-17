"""Async job queue for batch conversions"""

import json
from pathlib import Path
from datetime import datetime
import threading
import queue
import logging
from ..converters.pdf_processor import PDFProcessor
from ..converters.tts_engine import TTSEngine
from ..converters.audio_processor import AudioProcessor

logger = logging.getLogger(__name__)


class JobQueue:
    """Manages async conversion jobs"""
    
    def __init__(self, jobs_dir):
        self.jobs_dir = Path(jobs_dir)
        self.jobs_dir.mkdir(exist_ok=True)
        self.queue = queue.Queue()
        
        # Start worker thread
        self.worker_thread = threading.Thread(target=self._worker, daemon=True)
        self.worker_thread.start()
    
    def enqueue(self, job_data):
        """Add job to queue"""
        job_id = job_data["job_id"]
        job_file = self.jobs_dir / f"{job_id}.json"
        
        # Save job metadata
        with open(job_file, "w") as f:
            json.dump(job_data, f, indent=2)
        
        self.queue.put(job_id)
        logger.info(f"Queued job: {job_id}")
    
    def get_job(self, job_id):
        """Get job metadata and status"""
        job_file = self.jobs_dir / f"{job_id}.json"
        
        if not job_file.exists():
            raise KeyError(f"Job not found: {job_id}")
        
        with open(job_file, "r") as f:
            return json.load(f)
    
    def _update_job(self, job_id, updates):
        """Update job metadata"""
        job_data = self.get_job(job_id)
        job_data.update(updates)
        
        job_file = self.jobs_dir / f"{job_id}.json"
        with open(job_file, "w") as f:
            json.dump(job_data, f, indent=2)
    
    def _worker(self):
        """Background worker that processes queued jobs"""
        while True:
            try:
                job_id = self.queue.get()
                self._process_job(job_id)
            except Exception as e:
                logger.error(f"Worker error: {str(e)}")
    
    def _process_job(self, job_id):
        """Process a single job"""
        try:
            job_data = self.get_job(job_id)
            
            # Update status
            self._update_job(job_id, {
                "status": "processing",
                "started_at": datetime.now().isoformat()
            })
            
            # Step 1: Extract text
            logger.info(f"Extracting text from {job_data['filename']}")
            pdf_processor = PDFProcessor()
            text = pdf_processor.extract_text(job_data["file_path"])
            
            # Step 2: Synthesize speech
            logger.info(f"Synthesizing speech for job {job_id}")
            tts = TTSEngine()
            audio_path = tts.synthesize(
                text,
                engine=job_data["engine"],
                voice=job_data["voice"],
                output_dir=Path("outputs")
            )
            
            # Step 3: Process audio
            logger.info(f"Processing audio for job {job_id}")
            audio_processor = AudioProcessor()
            final_path = audio_processor.process_audio(
                audio_path,
                speed=job_data["speed"]
            )
            
            # Mark complete
            self._update_job(job_id, {
                "status": "completed",
                "completed_at": datetime.now().isoformat(),
                "output_file": str(final_path)
            })
            
            logger.info(f"Job completed: {job_id} -> {final_path}")
        
        except Exception as e:
            logger.error(f"Job failed: {job_id}: {str(e)}")
            self._update_job(job_id, {
                "status": "failed",
                "completed_at": datetime.now().isoformat(),
                "error": str(e)
            })
