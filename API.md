# PDF-to-Speech API Documentation

## Overview

REST API for converting PDFs to audio with configurable TTS engines, batch processing, and async job management.

## Base URL

```
http://localhost:5000/api
```

## Endpoints

### Health Check
```
GET /api/health
```
Returns: `{ "status": "healthy", "timestamp": "2026-03-17T21:00:00.000Z" }`

---

### List Available Voices
```
GET /api/voices?engine=gtts
```

**Query Parameters:**
- `engine` (optional): TTS engine - `gtts`, `system` (default: `gtts`)

**Response:**
```json
{
  "engine": "gtts",
  "voices": [
    { "id": "en", "name": "English (Google TTS)", "lang": "en" },
    { "id": "es", "name": "Spanish", "lang": "es" }
  ]
}
```

---

### Single File Conversion
```
POST /api/convert
Content-Type: multipart/form-data
```

**Form Parameters:**
- `file` (required): PDF file
- `engine` (optional): TTS engine - `gtts` or `system` (default: `gtts`)
- `voice` (optional): Voice ID/language code (default: `en`)
- `speed` (optional): Speech speed 0.5-2.0 (default: `1.0`)
- `async` (optional): Process asynchronously - `true` or `false` (default: `false`)

**Response (Synchronous):**
```json
{
  "job_id": "uuid-here",
  "status": "completed",
  "output_file": "/path/to/output.mp3",
  "download_url": "/api/download/uuid-here"
}
```

**Response (Asynchronous):**
```json
{
  "job_id": "uuid-here",
  "status": "queued",
  "message": "Conversion queued. Check status with /api/jobs/{job_id}"
}
```

---

### Batch Conversion
```
POST /api/batch
Content-Type: multipart/form-data
```

**Form Parameters:**
- `files` (required): Multiple PDF files
- `engine` (optional): TTS engine (default: `gtts`)
- `voice` (optional): Voice ID
- `speed` (optional): Speech speed 0.5-2.0 (default: `1.0`)

**Response:**
```json
{
  "job_count": 3,
  "job_ids": ["uuid-1", "uuid-2", "uuid-3"],
  "message": "All files queued for batch processing"
}
```

---

### Get Job Status
```
GET /api/jobs/{job_id}
```

**Response:**
```json
{
  "job_id": "uuid-here",
  "filename": "document.pdf",
  "file_path": "/path/to/document.pdf",
  "engine": "gtts",
  "voice": "en",
  "speed": 1.0,
  "status": "processing|completed|failed|queued",
  "created_at": "2026-03-17T21:00:00.000Z",
  "started_at": "2026-03-17T21:00:05.000Z",
  "completed_at": "2026-03-17T21:01:30.000Z",
  "output_file": "/path/to/output.mp3",
  "error": null
}
```

**Status Values:**
- `queued` - Waiting to be processed
- `processing` - Currently being converted
- `completed` - Successfully converted
- `failed` - Conversion error

---

### Download Audio File
```
GET /api/download/{job_id}
```

Downloads the converted MP3 file. Returns 404 if job not found or status not completed.

---

## Examples

### cURL - Single File

```bash
curl -X POST http://localhost:5000/api/convert \
  -F "file=@document.pdf" \
  -F "engine=gtts" \
  -F "voice=en" \
  -F "speed=1.0"
```

### cURL - Batch

```bash
curl -X POST http://localhost:5000/api/batch \
  -F "files=@doc1.pdf" \
  -F "files=@doc2.pdf" \
  -F "engine=gtts" \
  -F "speed=1.2"
```

### cURL - Check Job Status

```bash
curl http://localhost:5000/api/jobs/uuid-here
```

### JavaScript - Convert

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
console.log(job.job_id); // Track the job
```

### JavaScript - Poll Job Status

```javascript
function checkJobStatus(jobId) {
  fetch(`http://localhost:5000/api/jobs/${jobId}`)
    .then(r => r.json())
    .then(job => {
      if (job.status === "completed") {
        // Download link: /api/download/{jobId}
        console.log("Ready to download:", job.output_file);
      } else {
        console.log("Status:", job.status);
      }
    });
}
```

---

## Error Handling

All errors return JSON with an `error` field:

```json
{
  "error": "Invalid file type (must be PDF)"
}
```

**Common Status Codes:**
- `200` - Success (synchronous)
- `202` - Accepted (asynchronous)
- `400` - Bad request
- `404` - Not found
- `500` - Server error

---

## Best Practices

1. **Batch Processing**: Use `/batch` for multiple files to save API calls
2. **Async for Large Files**: Set `async=true` for PDFs > 10MB
3. **Poll Jobs**: Check status every 5-10 seconds instead of rapidly
4. **Voice Selection**: List voices first to provide UI options
5. **Speed Range**: Stay within 0.8-1.5 for natural speech

---

## Implementation Notes

- All timestamps are ISO 8601 format (UTC)
- File uploads max 100MB
- Temp files auto-cleanup after processing
- Job metadata persists in `jobs/` directory
- Audio files stored in `outputs/` directory
