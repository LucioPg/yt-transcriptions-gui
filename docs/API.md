# API Documentation

This document provides detailed API documentation for the YouTube Transcriptor library, covering both core modules, the FastAPI web interface, and the CLI executable.

## Table of Contents

- [Core Modules](#core-modules)
  - [transcriptor](#transcriptor)
  - [file_handler](#file_handler)
  - [utils](#utils)
  - [main](#main)
  - [web_app](#web_app)
- [CLI API](#cli-api)
  - [Command Reference](#command-reference)
  - [Exit Codes](#exit-codes)
  - [CLI Examples](#cli-examples)
- [Web API Endpoints](#web-api-endpoints)
- [Exceptions](#exceptions)
- [Data Structures](#data-structures)
- [Integration Examples](#integration-examples)

## Core Modules

### transcriptor

The main module for extracting YouTube video transcripts.

#### Functions

##### `get_transcript(video_url: str, language: str = None) -> List[Dict]`

Extract transcript from YouTube video.

**Parameters:**
- `video_url` (str): YouTube video URL
- `language` (str, optional): Language code (e.g., 'en', 'it'). If not specified, uses first available transcript

**Returns:**
- `List[Dict]`: List of transcript entries, each containing:
  - `text` (str): The transcript text
  - `start` (float): Start time in seconds
  - `duration` (float): Duration in seconds

**Raises:**
- `InvalidVideoURLError`: If URL is not a valid YouTube URL
- `NoTranscriptAvailableError`: If no transcript is available for the video

**Example:**
```python
from src.transcriptor import get_transcript

# Get transcript in default language
transcript = get_transcript("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

# Get transcript in specific language
transcript = get_transcript("https://www.youtube.com/watch?v=dQw4w9WgXcQ", language="en")
```

##### `get_video_title(video_url: str) -> str`

Get video title from YouTube URL.

**Parameters:**
- `video_url` (str): YouTube video URL

**Returns:**
- `str`: Video title

**Raises:**
- `InvalidVideoURLError`: If URL is not valid

**Example:**
```python
from src.transcriptor import get_video_title

title = get_video_title("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
print(f"Title: {title}")
```

#### Internal Functions

##### `_extract_video_id(url: str) -> str`

Extract video ID from YouTube URL.

**Parameters:**
- `url` (str): YouTube video URL

**Returns:**
- `str`: YouTube video ID

**Supported URL formats:**
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`

### file_handler

Module for handling file operations and transcript formatting.

#### Functions

##### `save_transcript(content: str, title: str, format_type: str, output_dir: str = "transcriptions") -> Path`

Save transcript content to file.

**Parameters:**
- `content` (str): Formatted transcript content
- `title` (str): Video title for filename generation
- `format_type` (str): File format (txt, srt, vtt)
- `output_dir` (str): Output directory path

**Returns:**
- `Path`: Path object pointing to the saved file

**Features:**
- Automatically creates output directory if it doesn't exist
- Sanitizes filename based on video title
- Handles filename conflicts by appending numbers

**Example:**
```python
from src.file_handler import save_transcript

filepath = save_transcript(
    content="Hello world transcript",
    title="Test Video: Episode 1",
    format_type="txt",
    output_dir="./transcripts"
)
print(f"Saved to: {filepath}")
```

##### `format_transcript(transcript_data: List[Dict], format_type: str) -> str`

Format transcript data according to specified format.

**Parameters:**
- `transcript_data` (List[Dict]): Raw transcript data from API
- `format_type` (str): Output format ("txt", "srt", "vtt")

**Returns:**
- `str`: Formatted transcript content

**Supported Formats:**

**TXT Format:**
- Plain text format
- Each transcript entry on a new line
- No timestamps

**SRT Format:**
- Subtitle format with sequence numbers
- Timestamps in HH:MM:SS,mmm format
- Compatible with most video players

**VTT Format:**
- Web Video Text Tracks format
- Timestamps in HH:MM:SS.mmm format
- Web-compatible subtitle format

**Example:**
```python
from src.file_handler import format_transcript

transcript_data = [
    {'text': 'Hello world', 'start': 0.0, 'duration': 2.5},
    {'text': 'This is a test', 'start': 2.5, 'duration': 3.0}
]

# Format as plain text
txt_content = format_transcript(transcript_data, "txt")

# Format as SRT
srt_content = format_transcript(transcript_data, "srt")

# Format as VTT
vtt_content = format_transcript(transcript_data, "vtt")
```

#### Internal Functions

##### `_format_srt(transcript_data) -> str`

Format transcript data as SRT subtitles.

##### `_format_vtt(transcript_data) -> str`

Format transcript data as VTT subtitles.

##### `_seconds_to_srt_time(seconds) -> str`

Convert seconds to SRT time format (HH:MM:SS,mmm).

##### `_seconds_to_vtt_time(seconds) -> str`

Convert seconds to VTT time format (HH:MM:SS.mmm).

### utils

Utility functions for validation and text processing.

#### Functions

##### `validate_youtube_url(url: str) -> bool`

Validate if URL is a valid YouTube URL.

**Parameters:**
- `url` (str): URL to validate

**Returns:**
- `bool`: True if valid YouTube URL, False otherwise

**Supported Patterns:**
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`

**Example:**
```python
from src.utils import validate_youtube_url

# Valid URLs
assert validate_youtube_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ") == True
assert validate_youtube_url("https://youtu.be/dQw4w9WgXcQ") == True

# Invalid URLs
assert validate_youtube_url("https://www.google.com") == False
assert validate_youtube_url("not-a-url") == False
```

##### `sanitize_filename(title: str) -> str`

Sanitize video title for valid filename.

**Parameters:**
- `title` (str): Video title to sanitize

**Returns:**
- `str`: Sanitized filename

**Processing:**
- Removes invalid characters: `< > : " / \ | ? *`
- Replaces spaces with underscores
- Limits filename length to 200 characters
- Preserves readability while ensuring filesystem compatibility

**Example:**
```python
from src.utils import sanitize_filename

filename = sanitize_filename("Test Video: Episode 1 - Introduction")
print(filename)  # Output: "Test_Video_Episode_1_-_Introduction"
```

### main

Command-line interface module.

#### Functions

##### `parse_arguments(args=None) -> argparse.Namespace`

Parse command line arguments.

**Parameters:**
- `args` (list, optional): List of arguments to parse (for testing)

**Returns:**
- `argparse.Namespace`: Parsed arguments object

**Arguments:**
- `url` (str): YouTube video URL (required)
- `--format, -f` (str): Output format (txt, srt, vtt) - default: txt
- `--language, -l` (str): Language code - default: auto-detect
- `--output, -o` (str): Output directory - default: transcriptions

##### `main(args=None) -> None`

Main CLI function that orchestrates the transcript extraction process.

**Process:**
1. Parse command line arguments
2. Validate YouTube URL
3. Extract transcript
4. Get video title
5. Format transcript
6. Save to file
7. Display summary

## CLI API

The CLI executable (`yt-transcriptor-cli.exe`) provides a command-line interface for transcript extraction with comprehensive argument parsing and error handling.

### Command Reference

#### Basic Usage

```bash
yt-transcriptor-cli.exe <URL> [OPTIONS]
```

#### Positional Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `<URL>` | Yes | YouTube video URL to extract transcript from |

#### Optional Arguments

| Option | Short | Description | Default | Example |
|--------|-------|-------------|---------|---------|
| `--format` | `-f` | Output format (txt, srt, vtt) | `txt` | `--format srt` |
| `--language` | `-l` | Language code (en, it, es, etc.) | auto-detect | `--language en` |
| `--output` | `-o` | Output directory | `transcriptions` | `--output "C:\Docs"` |
| `--help` | `-h` | Show help message and exit | - | `--help` |

#### Supported Output Formats

| Format | Extension | Description | Use Case |
|--------|-----------|-------------|----------|
| `txt` | `.txt` | Plain text transcript | Reading, documentation |
| `srt` | `.srt` | SubRip subtitle format | Video players, captioning |
| `vtt` | `.vtt` | WebVTT format | Web video, HTML5 players |

#### Supported Language Codes

| Code | Language | Code | Language |
|------|----------|------|----------|
| `en` | English | `es` | Spanish |
| `it` | Italian | `fr` | French |
| `de` | German | `pt` | Portuguese |
| `ru` | Russian | `ja` | Japanese |
| `ko` | Korean | `zh` | Chinese |
| `ar` | Arabic | `hi` | Hindi |

#### URL Formats Supported

```
https://www.youtube.com/watch?v=VIDEO_ID
https://youtu.be/VIDEO_ID
https://www.youtube.com/embed/VIDEO_ID
https://m.youtube.com/watch?v=VIDEO_ID
```

### Exit Codes

The CLI executable returns specific exit codes to indicate success or failure:

| Exit Code | Meaning | Description |
|-----------|---------|-------------|
| `0` | Success | Transcript extracted and saved successfully |
| `1` | Error | Invalid URL, no transcript available, or unexpected error |

#### Exit Code Usage Examples

```bash
# Check if extraction was successful
yt-transcriptor-cli.exe "https://youtu.be/VIDEO_ID"
if %ERRORLEVEL% EQU 0 (
    echo "Success: Transcript extracted"
) else (
    echo "Error: Failed to extract transcript"
)
```

```powershell
# PowerShell example
& "yt-transcriptor-cli.exe" "https://youtu.be/VIDEO_ID"
if ($LASTEXITCODE -eq 0) {
    Write-Host "Success: Transcript extracted"
} else {
    Write-Host "Error: Failed to extract transcript"
}
```

### CLI Examples

#### Basic Usage

```bash
# Extract transcript in default format (TXT)
yt-transcriptor-cli.exe "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```

**Output:**
```
Extracting transcript from: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Video title: Rick Astley - Never Gonna Give You Up (Official Music Video)
Transcript saved to: transcriptions/Rick_Astley_Never_Gonna_Give_You_Up_Official_Music_Video.txt
Format: txt
Lines: 162
```

#### Format Selection

```bash
# Extract as SRT subtitles
yt-transcriptor-cli.exe "https://youtu.be/dQw4w9WgXcQ" --format srt

# Extract as VTT web subtitles
yt-transcriptor-cli.exe "https://youtu.be/dQw4w9WgXcQ" -f vtt
```

#### Language Selection

```bash
# Extract English transcript specifically
yt-transcriptor-cli.exe "https://youtu.be/dQw4w9WgXcQ" --language en

# Extract Spanish transcript
yt-transcriptor-cli.exe "https://youtu.be/dQw4w9WgXcQ" -l es
```

#### Custom Output Directory

```bash
# Save to custom directory
yt-transcriptor-cli.exe "https://youtu.be/dQw4w9WgXcQ" --output "C:\My Documents\Transcripts"

# Save to relative directory
yt-transcriptor-cli.exe "https://youtu.be/dQw4w9WgXcQ" -o ./subtitles
```

#### Combined Options

```bash
# All options together
yt-transcriptor-cli.exe "https://youtu.be/dQw4w9WgXcQ" \
  --format srt \
  --language en \
  --output "C:\Subtitles"
```

#### Error Handling Examples

```bash
# Invalid URL
yt-transcriptor-cli.exe "not-a-url"
# Output: Error: Invalid YouTube URL: not-a-url

# Video without transcript
yt-transcriptor-cli.exe "https://youtu.be/VIDEO_WITH_NO_CAPTIONS"
# Output: Error: No transcript available for this video
```

#### Help Command

```bash
# Show help message
yt-transcriptor-cli.exe --help
```

**Output:**
```
usage: yt-transcriptor-cli.exe [-h] [--format {txt,srt,vtt}] [--language LANGUAGE]
                               [--output OUTPUT]
                               url

Extract YouTube video transcripts

positional arguments:
  url                   YouTube video URL

options:
  -h, --help            show this help message and exit
  --format {txt,srt,vtt}, -f {txt,srt,vtt}
                        Output format (default: txt)
  --language LANGUAGE, -l LANGUAGE
                        Language code (e.g., en, it, es). If not specified, uses first available.
  --output OUTPUT, -o OUTPUT
                        Output directory (default: transcriptions)

Examples:
  yt-transcriptor-cli.exe "https://youtu.be/dQw4w9WgXcQ"
  yt-transcriptor-cli.exe "https://youtu.be/dQw4w9WgXcQ" --format srt
  yt-transcriptor-cli.exe "https://youtu.be/dQw4w9WgXcQ" --language en --output ./transcripts
```

### CLI Integration Examples

#### Batch Processing (Windows)

```batch
@echo off
echo Processing multiple videos...

yt-transcriptor-cli.exe "https://www.youtube.com/watch?v=VIDEO1" --format srt
if %ERRORLEVEL% EQU 0 (
    echo ✓ VIDEO1 processed successfully
) else (
    echo ✗ VIDEO1 failed
)

yt-transcriptor-cli.exe "https://www.youtube.com/watch?v=VIDEO2" --format txt
if %ERRORLEVEL% EQU 0 (
    echo ✓ VIDEO2 processed successfully
) else (
    echo ✗ VIDEO2 failed
)

echo Batch processing complete
```

#### PowerShell Script

```powershell
# Process URLs from a file
$urls = Get-Content "video_urls.txt"
$outputDir = "C:\Transcripts"

foreach ($url in $urls) {
    Write-Host "Processing: $url"

    $process = Start-Process -FilePath "yt-transcriptor-cli.exe" -ArgumentList $url, "--output", $outputDir -Wait -PassThru

    if ($process.ExitCode -eq 0) {
        Write-Host "✓ Success: $url" -ForegroundColor Green
    } else {
        Write-Host "✗ Failed: $url" -ForegroundColor Red
    }
}
```

#### Python Subprocess Integration

```python
import subprocess
import json

def extract_transcript_cli(url, format_type="txt", language=None, output_dir=None):
    """Extract transcript using CLI executable."""

    cmd = ["yt-transcriptor-cli.exe", url]

    if format_type:
        cmd.extend(["--format", format_type])
    if language:
        cmd.extend(["--language", language])
    if output_dir:
        cmd.extend(["--output", output_dir])

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )

        return {
            "success": True,
            "output": result.stdout,
            "error": result.stderr
        }

    except subprocess.CalledProcessError as e:
        return {
            "success": False,
            "output": e.stdout,
            "error": e.stderr,
            "exit_code": e.returncode
        }

# Usage example
result = extract_transcript_cli(
    "https://youtu.be/dQw4w9WgXcQ",
    format_type="srt",
    language="en",
    output_dir="./transcripts"
)

if result["success"]:
    print("Transcript extracted successfully!")
    print(result["output"])
else:
    print("Extraction failed!")
    print(f"Error: {result['error']}")
    print(f"Exit code: {result['exit_code']}")
```

### CLI Error Messages

The CLI provides specific error messages for different failure scenarios:

#### Invalid URL Error
```
Error: Invalid YouTube URL: INVALID_URL
```
**Cause**: The provided URL is not a valid YouTube URL format.

#### No Transcript Error
```
Error: No transcript available for this video: REASON
```
**Cause**: The video doesn't have captions or transcripts available.

#### Network/Connection Error
```
Error: Network error: CONNECTION_ERROR_MESSAGE
```
**Cause**: Unable to connect to YouTube or transcript service.

#### File System Error
```
Error: File system error: ERROR_MESSAGE
```
**Cause**: Permission denied, disk full, or invalid output path.

### web_app

FastAPI web application module providing browser-based transcript extraction interface.

#### Application Setup

##### `app = FastAPI(...)`

FastAPI application instance with configuration:

**Parameters:**
- `title`: "YouTube Transcriptor"
- `description`: "Extract YouTube video transcripts directly without downloading videos"
- `version`: "1.0.0"
- `lifespan`: Application lifespan manager for cleanup

**Features:**
- Automatic API documentation at `/docs`
- Template rendering with Jinja2
- Static file serving
- Temporary file management

#### Web Endpoints

The web application provides the following HTTP endpoints:

##### `GET /` → HTMLResponse

Render the homepage with transcript extraction form.

**Returns:**
- HTML page with form interface
- Template: `index.html`
- Context: Basic navigation and form data

**Example Request:**
```bash
curl http://localhost:8000/
```

##### `POST /extract` → HTMLResponse

Process transcript extraction from form submission.

**Parameters:**
- `url` (form): YouTube video URL (required)
- `format_type` (form): Output format (txt/srt/vtt, default: txt)
- `language` (form): Language code (optional)

**Returns:**
- Success: HTML with transcript preview and download link
- Error: HTML with error message and guidance

**Example Request:**
```bash
curl -X POST http://localhost:8000/extract \
  -F "url=https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  -F "format_type=srt" \
  -F "language=en"
```

##### `GET /download/{filename}` → FileResponse

Download transcript file.

**Parameters:**
- `filename` (path): Name of file to download

**Returns:**
- File download with appropriate MIME type
- Security: Validates file is in temporary directory

**Example Request:**
```bash
curl -O http://localhost:8000/download/video_title_srt.txt
```

##### `GET /health` → JSON

Health check endpoint for monitoring.

**Returns:**
```json
{
  "status": "healthy",
  "service": "YouTube Transcriptor"
}
```

#### Template Integration

##### `templates = Jinja2Templates("src/templates")`

Jinja2 template engine setup for HTML rendering.

**Available Templates:**
- `base.html`: Base layout with styling and navigation
- `index.html`: Homepage with extraction form
- `result.html`: Results display with success/error states

#### Static Files

##### `app.mount("/static", StaticFiles("src/static"))`

Static file serving for CSS, JavaScript, and images.

**Usage in Templates:**
```html
<link rel="stylesheet" href="/static/css/custom.css">
```

#### Error Handling

The web application provides comprehensive error handling:

**Error Types:**
- `InvalidVideoURLError`: Invalid YouTube URL format
- `NoTranscriptAvailableError`: No transcript available for video
- `Exception`: Unexpected system errors

**Error Response Context:**
```python
{
    "request": request,
    "success": False,
    "error": "Error description",
    "error_type": "invalid_url" | "no_transcript" | "unexpected"
}
```

#### File Management

##### `TEMP_DIR = Path(tempfile.mkdtemp(prefix="yt_transcriptor_"))`

Temporary directory for file downloads with automatic cleanup.

**Features:**
- Secure temporary file handling
- Automatic cleanup on application shutdown
- Conflict resolution for duplicate files

## Web API Endpoints

The YouTube Transcriptor web interface provides a RESTful API built on FastAPI. All endpoints return HTML responses for browser compatibility.

### Base URL
```
http://localhost:8000
```

### Available Endpoints

#### GET /

Renders the homepage with the transcript extraction form.

**Response:** HTML page with form interface

**Example:**
```bash
# Get homepage
curl http://localhost:8000/

# Open in browser
open http://localhost:8000
```

#### POST /

Process transcript extraction request (alias for `/extract`).

**Content-Type:** `application/x-www-form-urlencoded`

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `url` | string | Yes | YouTube video URL |
| `format_type` | string | No | Output format (txt, srt, vtt) |
| `language` | string | No | Language code (e.g., en, it, es) |

**Example Request:**
```bash
curl -X POST http://localhost:8000/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "url=https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  -d "format_type=srt" \
  -d "language=en"
```

#### POST /extract

Process transcript extraction request (primary endpoint).

**Content-Type:** `application/x-www-form-urlencoded`

**Parameters:**
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `url` | string | Yes | - | YouTube video URL |
| `format_type` | string | No | txt | Output format (txt/srt/vtt) |
| `language` | string | No | auto | Language code preference |

**Success Response (200 OK):**
```html
<!-- HTML with transcript preview and download options -->
<div class="success-message">
    <strong>✅ Trascrizione estratta con successo!</strong>
</div>
<div class="video-info">
    <h3>📹 Informazioni Video</h3>
    <p><strong>Titolo:</strong> Video Title</p>
    <p><strong>URL:</strong> <a href="...">https://...</a></p>
</div>
<div class="transcript-content">...</div>
<a href="/download/filename.srt" role="button" class="primary">
    💾 Scarica SRT
</a>
```

**Error Response (200 OK):**
```html
<!-- HTML with error message and guidance -->
<div class="error-message">
    <h3>❌ Si è verificato un errore</h3>
    <p><strong>URL non valido</strong></p>
    <p>The provided URL is not a valid YouTube URL.</p>
</div>
```

**Example Request:**
```bash
# Basic extraction
curl -X POST http://localhost:8000/extract \
  -d "url=https://youtu.be/dQw4w9WgXcQ"

# With format and language
curl -X POST http://localhost:8000/extract \
  -d "url=https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  -d "format_type=vtt" \
  -d "language=it"
```

#### GET /download/{filename}

Download transcript file generated from extraction.

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `filename` | string | Name of file to download |

**Response:** File download with appropriate MIME type

**Headers:**
```
Content-Type: text/plain
Content-Disposition: attachment; filename="video_title.txt"
```

**Example Request:**
```bash
# Download file
curl -O http://localhost:8000/download/video_title_srt.txt

# Download with custom filename
curl -o my_transcript.srt http://localhost:8000/download/video_title_srt.txt
```

**Security Note:** Files are validated to ensure they exist in the temporary directory to prevent path traversal attacks.

#### GET /health

Health check endpoint for monitoring and load balancers.

**Response:** JSON status information

**Example Response:**
```json
{
  "status": "healthy",
  "service": "YouTube Transcriptor"
}
```

**Example Request:**
```bash
curl http://localhost:8000/health

# Response
{"status":"healthy","service":"YouTube Transcriptor"}
```

### URL Formats Supported

All endpoints accept the following YouTube URL formats:

```
https://www.youtube.com/watch?v=VIDEO_ID
https://youtu.be/VIDEO_ID
https://www.youtube.com/embed/VIDEO_ID
https://m.youtube.com/watch?v=VIDEO_ID
```

### Response Formats

#### HTML Responses

Most endpoints return HTML responses for browser compatibility:

```html
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <title>YouTube Transcriptor</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@1/css/pico.min.css">
</head>
<body>
    <!-- Content -->
</body>
</html>
```

#### File Responses

Download endpoints return raw files:

```http
HTTP/1.1 200 OK
Content-Type: text/plain
Content-Disposition: attachment; filename="video_title.txt"
Content-Length: 1234

[File content...]
```

#### JSON Responses

Health check returns JSON:

```json
{
  "status": "healthy",
  "service": "YouTube Transcriptor"
}
```

### Error Handling

#### HTTP Status Codes

| Status Code | Description | Usage |
|-------------|-------------|-------|
| 200 OK | Success | All successful responses |
| 404 Not Found | File not found | Invalid download filename |
| 422 Unprocessable Entity | Validation error | Invalid form data |

#### Error Response Format

Errors are returned as HTML with user-friendly messages:

```html
<div class="error-message">
    <h3>❌ Si è verificato un errore</h3>

    {% if error_type == "invalid_url" %}
    <p><strong>URL non valido</strong></p>
    <p>{{ error }}</p>

    {% elif error_type == "no_transcript" %}
    <p><strong>Trascrizione non disponibile</strong></p>
    <p>{{ error }}</p>

    {% else %}
    <p><strong>Errore imprevisto</strong></p>
    <p>{{ error }}</p>
    {% endif %}
</div>
```

#### Error Types

| Error Type | Description | Causes |
|------------|-------------|---------|
| `invalid_url` | Invalid YouTube URL format | Malformed URL, unsupported format |
| `no_transcript` | No transcript available | Video lacks captions, private video |
| `unexpected` | System error | Network issues, API failures |

### Integration Examples

#### Python Integration

```python
import requests
from pathlib import Path

def extract_transcript_web_api(youtube_url, format_type="txt", language=None):
    """Extract transcript using web API."""

    # Prepare form data
    data = {
        "url": youtube_url,
        "format_type": format_type,
    }
    if language:
        data["language"] = language

    # Submit extraction request
    response = requests.post("http://localhost:8000/extract", data=data)
    response.raise_for_status()

    # Extract download link from HTML response (simplified)
    if "download/" in response.text:
        # Parse HTML to find download link
        download_url = "http://localhost:8000/download/filename.txt"

        # Download file
        file_response = requests.get(download_url)
        file_response.raise_for_status()

        return file_response.text
    else:
        raise Exception("Extraction failed")

# Usage
transcript = extract_transcript_web_api(
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    format_type="srt",
    language="en"
)
print(transcript)
```

#### JavaScript Integration

```javascript
async function extractTranscript(url, format = 'txt', language = null) {
    const formData = new FormData();
    formData.append('url', url);
    formData.append('format_type', format);
    if (language) {
        formData.append('language', language);
    }

    try {
        const response = await fetch('/extract', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const html = await response.text();

        // Parse HTML to find download link (simplified)
        const downloadMatch = html.match(/href="\/download\/([^"]+)"/);
        if (downloadMatch) {
            const filename = downloadMatch[1];
            const downloadUrl = `/download/${filename}`;

            // Trigger download
            const a = document.createElement('a');
            a.href = downloadUrl;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        }

    } catch (error) {
        console.error('Error extracting transcript:', error);
        throw error;
    }
}

// Usage
extractTranscript(
    'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    'srt',
    'en'
);
```

#### cURL Examples

```bash
#!/bin/bash

# Extract transcript with cURL
YOUTUBE_URL="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
FORMAT="srt"
LANGUAGE="en"

# Submit extraction request
RESPONSE=$(curl -s -X POST "http://localhost:8000/extract" \
    -d "url=$YOUTUBE_URL" \
    -d "format_type=$FORMAT" \
    -d "language=$LANGUAGE")

# Check for success
if [[ $RESPONSE == *"Trascrizione estratta con successo"* ]]; then
    echo "Extraction successful!"

    # Extract filename (simplified)
    FILENAME=$(echo "$RESPONSE" | grep -o 'download/[^"]*' | cut -d'/' -f2)

    if [ ! -z "$FILENAME" ]; then
        echo "Downloading: $FILENAME"
        curl -O "http://localhost:8000/download/$FILENAME"
        echo "Download complete!"
    fi
else
    echo "Extraction failed"
    echo "$RESPONSE"
fi
```

## Exceptions

### Custom Exceptions

#### `InvalidVideoURLError`

Raised when the provided URL is not a valid YouTube URL.

```python
from src.transcriptor import InvalidVideoURLError

try:
    get_transcript("invalid-url")
except InvalidVideoURLError as e:
    print(f"Error: {e}")
```

#### `NoTranscriptAvailableError`

Raised when no transcript is available for a video.

```python
from src.transcriptor import NoTranscriptAvailableError

try:
    get_transcript("https://www.youtube.com/watch?v=NO_TRANSCRIPT")
except NoTranscriptAvailableError as e:
    print(f"Error: {e}")
```

## Data Structures

### Transcript Entry

Each transcript entry is a dictionary or object with the following structure:

```python
{
    'text': str,      # The transcript text content
    'start': float,   # Start time in seconds
    'duration': float # Duration in seconds
}
```

### Example Usage

```python
from src.transcriptor import get_transcript, get_video_title
from src.file_handler import save_transcript, format_transcript

# Extract transcript
transcript_data = get_transcript("https://www.youtube.com/watch?v=VIDEO_ID")

# Get video title
title = get_video_title("https://www.youtube.com/watch?v=VIDEO_ID")

# Format as SRT
srt_content = format_transcript(transcript_data, "srt")

# Save to file
filepath = save_transcript(srt_content, title, "srt", "./transcripts")

print(f"Transcript saved to: {filepath}")
```

## Error Handling Best Practices

```python
from src.transcriptor import get_transcript, NoTranscriptAvailableError, InvalidVideoURLError
from src.utils import validate_youtube_url

def safe_transcript_extraction(url, language=None):
    """Safely extract transcript with comprehensive error handling."""

    # Validate URL first
    if not validate_youtube_url(url):
        raise InvalidVideoURLError(f"Invalid YouTube URL: {url}")

    try:
        transcript = get_transcript(url, language)
        return transcript
    except NoTranscriptAvailableError:
        print(f"No transcript available for: {url}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
```