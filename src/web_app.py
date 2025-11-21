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

from starlette.middleware.cors import CORSMiddleware

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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # oppure ["*"] per test
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# API-only mode: no static files or templates when called by Tauri
# Templates and static files are only served when running standalone
import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    # Running as PyInstaller executable - API only mode for Tauri
    pass  # Don't mount static files or templates
else:
    # Running as script - serve full web interface
    base_dir = Path(__file__).parent
    app.mount("/static", StaticFiles(directory=str(base_dir / "static")), name="static")
    templates = Jinja2Templates(directory=str(base_dir / "templates"))

# Temporary directory for file downloads
TEMP_DIR = Path(tempfile.mkdtemp(prefix="yt_transcriptor_"))


# API routes - always available
@app.get("/")
async def index():
    """Root endpoint - API info."""
    return {
        "service": "YouTube Transcriptor API",
        "version": "1.0.0",
        "endpoints": {
            "/health": "Health check",
            "/api/transcript": "Extract transcript (POST)"
        }
    }

# HTML routes only when running standalone
if not getattr(sys, 'frozen', False):
    @app.get("/web", response_class=HTMLResponse)
    async def index_web(request: Request):
        """Render the homepage with the URL input form."""
        return templates.TemplateResponse(request, "index.html")

    @app.post("/extract", response_class=HTMLResponse)
    async def extract_transcript_web(
        request: Request,
        url: str = Form(...),
        format_type: str = Form(default="txt"),
        language: Optional[str] = Form(default=None)
    ):
        """
        Extract transcript from YouTube URL and display results (web interface).
        """
        try:
            # Validate YouTube URL
            if not validate_youtube_url(url):
                return templates.TemplateResponse(
                    "index.html",
                    {"request": request, "error": "Invalid YouTube URL. Please check and try again."}
                )

            # Extract transcript
            transcript = get_transcript(url, language=language)
            video_title = get_video_title(url)

            # Format and save transcript
            formatted_transcript = format_transcript(transcript, format_type)
            saved_file = save_transcript(formatted_transcript, video_title, format_type)

            return templates.TemplateResponse(
                "result.html",
                {
                    "request": request,
                    "video_title": video_title,
                    "transcript": formatted_transcript,
                    "filename": saved_file
                }
            )

        except NoTranscriptAvailableError:
            return templates.TemplateResponse(
                "index.html",
                {"request": request, "error": f"No transcript available for this video. {str(e)}"}
            )
        except InvalidVideoURLError:
            return templates.TemplateResponse(
                "index.html",
                {"request": request, "error": "Invalid YouTube video URL. Please check and try again."}
            )
        except Exception as e:
            return templates.TemplateResponse(
                "index.html",
                {"request": request, "error": f"Error extracting transcript: {str(e)}"}
            )


# API-only endpoint for Tauri
@app.post("/api/transcript")
async def extract_transcript_api(
    url: str = Form(...),
    format_type: str = Form(default="txt"),
    language: Optional[str] = Form(default=None)
):
    """
    API endpoint to extract transcript from YouTube URL.
    Returns JSON response for Tauri frontend.
    """
    try:
        # Validate YouTube URL
        if not validate_youtube_url(url):
            return {"error": "Invalid YouTube URL. Please check and try again."}

        # Extract transcript
        transcript = get_transcript(url, language=language)
        video_title = get_video_title(url)

        # Format and save transcript
        formatted_transcript = format_transcript(transcript, format_type)
        saved_file = save_transcript(formatted_transcript, video_title, format_type)

        return {
            "success": True,
            "video_title": video_title,
            "transcript": formatted_transcript,
            "filename": saved_file
        }

    except NoTranscriptAvailableError as e:
        return {"error": f"No transcript available for this video. {str(e)}"}
    except InvalidVideoURLError:
        return {"error": "Invalid YouTube video URL. Please check and try again."}
    except Exception as e:
        return {"error": f"Error extracting transcript: {str(e)}"}

# HTML endpoint for standalone web mode
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

@app.post("/shutdown")
async def shutdown():
    """Shutdown the backend server."""
    import threading

    def delayed_shutdown():
        import time
        time.sleep(0.5)  # Give time for response to be sent
        import sys
        sys.exit(0)

    # Run shutdown in a separate thread to avoid blocking the response
    threading.Thread(target=delayed_shutdown, daemon=True).start()
    return {"message": "Shutting down backend server"}




if __name__ == "__main__":
    import uvicorn

    print("🚀 Starting YouTube Transcriptor Web Interface")
    print("📍 Open http://localhost:8031 in your browser")
    print("📖 Documentation: http://localhost:8031/docs")
    print("🛑 Press Ctrl+C to stop the server")

    # Fix module path for PyInstaller
    import sys
    from pathlib import Path

    if getattr(sys, 'frozen', False):
        # Add current directory to Python path when running as PyInstaller executable
        current_dir = Path(sys.executable).parent
        if str(current_dir) not in sys.path:
            sys.path.insert(0, str(current_dir))

    # Use direct app reference instead of string
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8031,
        reload=False,
        log_level="info"
    )
