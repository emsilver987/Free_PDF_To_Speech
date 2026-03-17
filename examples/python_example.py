"""
Python integration example for PDF-to-Speech API
"""

import requests
import time
import json
from pathlib import Path

API_BASE = "http://localhost:5000/api"


def convert_single_file(pdf_path, async_mode=True):
    """Convert a single PDF to speech"""
    print(f"Converting {pdf_path}...")
    
    with open(pdf_path, "rb") as f:
        response = requests.post(
            f"{API_BASE}/convert",
            files={"file": f},
            data={
                "engine": "gtts",
                "voice": "en",
                "speed": 1.0,
                "async": async_mode
            }
        )
    
    if response.status_code in [200, 202]:
        data = response.json()
        print(f"✅ Job created: {data['job_id']}")
        print(f"   Status: {data['status']}")
        
        if async_mode:
            return data["job_id"]
        else:
            print(f"   Download: {data['download_url']}")
            return data["job_id"]
    else:
        print(f"❌ Error: {response.json()}")
        return None


def batch_convert(pdf_paths, engine="gtts", speed=1.0):
    """Convert multiple PDFs in batch"""
    print(f"Converting {len(pdf_paths)} files...")
    
    files = []
    for path in pdf_paths:
        files.append(("files", open(path, "rb")))
    
    response = requests.post(
        f"{API_BASE}/batch",
        files=files,
        data={
            "engine": engine,
            "speed": speed
        }
    )
    
    if response.status_code == 202:
        data = response.json()
        print(f"✅ Batch submitted")
        print(f"   Files: {data['job_count']}")
        print(f"   Job IDs: {data['job_ids']}")
        return data["job_ids"]
    else:
        print(f"❌ Error: {response.json()}")
        return []


def check_job_status(job_id):
    """Check status of a conversion job"""
    response = requests.get(f"{API_BASE}/jobs/{job_id}")
    
    if response.status_code == 200:
        job = response.json()
        return job
    else:
        print(f"❌ Job not found: {job_id}")
        return None


def wait_for_job(job_id, max_wait_seconds=300, poll_interval=5):
    """Wait for job to complete with polling"""
    print(f"\n⏳ Waiting for job {job_id}...")
    
    start = time.time()
    while time.time() - start < max_wait_seconds:
        job = check_job_status(job_id)
        
        if not job:
            return False
        
        status = job["status"]
        print(f"   Status: {status}")
        
        if status == "completed":
            print(f"✅ Job completed!")
            print(f"   Output: {job['output_file']}")
            return True
        elif status == "failed":
            print(f"❌ Job failed: {job['error']}")
            return False
        
        time.sleep(poll_interval)
    
    print(f"⏱️  Timeout waiting for job")
    return False


def download_job(job_id, output_path):
    """Download completed job"""
    response = requests.get(f"{API_BASE}/download/{job_id}")
    
    if response.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"✅ Downloaded: {output_path}")
        return True
    else:
        print(f"❌ Download failed: {response.json()}")
        return False


def list_voices(engine="gtts"):
    """List available voices for an engine"""
    response = requests.get(f"{API_BASE}/voices?engine={engine}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n🎤 Available voices ({engine}):")
        for voice in data["voices"]:
            print(f"   {voice['id']}: {voice['name']}")
        return data["voices"]
    else:
        print(f"❌ Error: {response.json()}")
        return []


# Example usage
if __name__ == "__main__":
    import sys
    
    # Check health
    try:
        response = requests.get(f"{API_BASE}/health")
        print(f"✅ API healthy: {response.json()['status']}\n")
    except requests.exceptions.ConnectionError:
        print("❌ API not running. Start with: python backend/app.py")
        sys.exit(1)
    
    # Example 1: List available voices
    print("=" * 50)
    print("EXAMPLE 1: List Available Voices")
    print("=" * 50)
    list_voices("gtts")
    list_voices("system")
    
    # Example 2: Convert single file (async)
    print("\n" + "=" * 50)
    print("EXAMPLE 2: Convert Single File (Async)")
    print("=" * 50)
    
    # Create a test PDF if it doesn't exist
    test_pdf = "test_document.pdf"
    if not Path(test_pdf).exists():
        print(f"⚠️  {test_pdf} not found. Create one first.")
    else:
        job_id = convert_single_file(test_pdf, async_mode=True)
        
        if job_id:
            # Wait for completion
            if wait_for_job(job_id):
                download_job(job_id, "output_async.mp3")
    
    # Example 3: Batch processing
    print("\n" + "=" * 50)
    print("EXAMPLE 3: Batch Processing")
    print("=" * 50)
    
    pdf_files = [
        "test_document.pdf",
        "another_document.pdf"
    ]
    pdf_files = [p for p in pdf_files if Path(p).exists()]
    
    if pdf_files:
        job_ids = batch_convert(pdf_files, engine="system", speed=1.2)
        
        # Wait for all jobs
        for job_id in job_ids:
            if wait_for_job(job_id):
                download_job(job_id, f"output_{job_id[:8]}.mp3")
    else:
        print("⚠️  No test PDFs found. Create some first.")
    
    print("\n✅ Done!")
