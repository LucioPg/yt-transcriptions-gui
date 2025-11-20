"""
YouTube Transcriptor Web Interface

A minimal, clean web interface for extracting YouTube video transcripts
using FastAPI and Pico.css for styling.
"""

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from typing import Optional
import tempfile
import shutil

from src.transcriptor import (get_transcript, get_video_title, NoTranscriptAvailableError,
                            InvalidVideoURLError)
from src.file_handler import format_transcript, save_transcript
from src.utils import validate_youtube_url

# Initialize FastAPI app with lifespan
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    yield  # Application runs
    # Cleanup on shutdown
    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR, ignore_errors=True)

app = FastAPI(
    title="YouTube Transcriptor",
    description="Extract YouTube video transcripts directly without downloading videos",
    version="1.0.0",
    lifespan=lifespan
)

# Mount static files and setup templates
app.mount("/static", StaticFiles(directory="./static"), name="static")
templates = Jinja2Templates(directory="./templates")

# Temporary directory for file downloads
TEMP_DIR = Path(tempfile.mkdtemp(prefix="yt_transcriptor_"))


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render the homepage with the URL input form."""
    return templates.TemplateResponse(request, "index.html")


@app.post("/extract", response_class=HTMLResponse)
async def extract_transcript(
    request: Request,
    url: str = Form(...),
    format_type: str = Form(default="txt"),
    language: Optional[str] = Form(default=None)
):
    """
    Extract transcript from YouTube URL and display results.

    Args:
        request: FastAPI request object
        url: YouTube video URL
        format_type: Output format (txt, srt, vtt)
        language: Optional language code

    Returns:
        HTML response with results or error message
    """
    try:
        # Validate URL
        if not validate_youtube_url(url):
            raise InvalidVideoURLError("Invalid YouTube URL")

        # Extract transcript
        transcript_data = get_transcript(url, language)

        # Get video title
        video_title = get_video_title(url)

        # Format transcript
        formatted_content = format_transcript(transcript_data, format_type)

        # Save to temporary file for download
        temp_file = save_transcript(
            formatted_content,
            video_title,
            format_type,
            str(TEMP_DIR)
        )

        # Prepare response data
        context = {
            "request": request,
            "success": True,
            "video_title": video_title,
            "video_url": url,
            "transcript_content": formatted_content,
            "format_type": format_type,
            "language": language,
            "download_filename": temp_file.name,
            "lines_count": len(transcript_data)
        }

    except InvalidVideoURLError as e:
        context = {
            "request": request,
            "success": False,
            "error": str(e),
            "error_type": "invalid_url"
        }

    except NoTranscriptAvailableError as e:
        context = {
            "request": request,
            "success": False,
            "error": str(e),
            "error_type": "no_transcript"
        }

    except Exception as e:
        context = {
            "request": request,
            "success": False,
            "error": f"Unexpected error: {str(e)}",
            "error_type": "unexpected"
        }

    return templates.TemplateResponse(request, "result.html", context)


@app.get("/download/{filename}")
async def download_file(filename: str):
    """Download the transcript file."""
    file_path = TEMP_DIR / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='text/plain'
    )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "YouTube Transcriptor"}




if __name__ == "__main__":
    import uvicorn

    print("🚀 Starting YouTube Transcriptor Web Interface")
    print("📍 Open http://localhost:8031 in your browser")
    print("📖 Documentation: http://localhost:8031/docs")
    print("🛑 Press Ctrl+C to stop the server")

    uvicorn.run(
        "web_app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
