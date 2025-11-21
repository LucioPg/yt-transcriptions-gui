# src/web_main.py
"""
YouTube Transcriptor Web Interface Main Entry Point

Windows native executable entry point for the web interface.
Saves transcripts to user's home directory under yt-transcriptions.
"""

import sys
import webbrowser
from pathlib import Path
import time

# Add src to path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from transcriptor import get_transcript, get_video_title, NoTranscriptAvailableError, InvalidVideoURLError
from file_handler import format_transcript, save_transcript
from utils import validate_youtube_url

def ensure_download_directory():
    """Ensure the download directory exists for web interface."""
    try:
        home = Path.home()
        download_dir = home / "yt-transcriptions"
        download_dir.mkdir(exist_ok=True)

        # Create a README file if it doesn't exist
        readme_file = download_dir / "README.txt"
        if not readme_file.exists():
            readme_content = """# YouTube Transcriptor Download Directory

This directory contains transcripts downloaded by YouTube Transcriptor Web Interface.

## Files in this directory
- Files are named using the YouTube video title
- Multiple formats are supported: .txt, .srt, .vtt
- Each file contains the complete transcript of the corresponding video

## Managing files
- You can safely delete files you no longer need
- The directory will be automatically recreated if deleted
- Files are downloaded when you use the "Download" button in the web interface

## Questions
If you have questions about YouTube Transcriptor, please refer to the project documentation.
"""
            with open(readme_file, 'w', encoding='utf-8') as f:
                f.write(readme_content)

        return True, str(download_dir)

    except Exception as e:
        return False, str(e)
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import tempfile
import shutil

def get_default_download_dir():
    """Get the default download directory for transcripts."""
    home = Path.home()
    download_dir = home / "yt-transcriptions"
    download_dir.mkdir(exist_ok=True)
    return str(download_dir)

def create_modified_app():
    """Create a modified FastAPI app that uses permanent download directory."""
    # Import the original app configuration
    from contextlib import asynccontextmanager

    # Use permanent download directory instead of temp
    PERMANENT_DIR = Path(get_default_download_dir())

    @asynccontextmanager
    async def lifespan(app_instance: FastAPI):
        """Application lifespan manager."""
        yield  # Application runs
        # Cleanup not needed for permanent directory

    # Create new app with modified behavior
    modified_app = FastAPI(
        title="YouTube Transcriptor",
        description="Extract YouTube video transcripts directly without downloading videos",
        version="1.0.0",
        lifespan=lifespan
    )

    # Mount static files and setup templates
    current_dir = Path(__file__).parent
    static_dir = current_dir / "static"
    templates_dir = current_dir / "templates"

    # Try to mount static files if directory exists
    if static_dir.exists():
        modified_app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    templates = Jinja2Templates(directory=str(templates_dir))

    @modified_app.get("/", response_class=HTMLResponse)
    async def index(request: Request):
        """Render the homepage with the URL input form."""
        return templates.TemplateResponse(request, "index.html")

    @modified_app.post("/extract", response_class=HTMLResponse)
    async def extract_transcript(
        request: Request,
        url: str = Form(...),
        format_type: str = Form(default="txt"),
        language: str | None = Form(default=None)
    ):
        """Extract transcript from YouTube URL and display results."""
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

            # Save to permanent directory
            temp_file = save_transcript(
                formatted_content,
                video_title,
                format_type,
                str(PERMANENT_DIR)
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
                "lines_count": len(transcript_data),
                "download_path": str(PERMANENT_DIR)
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

    @modified_app.get("/download/{filename}")
    async def download_file(filename: str):
        """Download the transcript file."""
        file_path = PERMANENT_DIR / filename

        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")

        return FileResponse(
            path=file_path,
            filename=filename,
            media_type='text/plain'
        )

    @modified_app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {"status": "healthy", "service": "YouTube Transcriptor"}

    return modified_app

def open_browser(url: str, delay: float = 1.5):
    """Open browser after a delay to ensure server is ready."""
    time.sleep(delay)
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"Could not open browser automatically: {e}")
        print(f"Please open this URL manually: {url}")

def main():
    """Main entry point for yt-transcriptor-web."""
    import uvicorn

    print("Starting YouTube Transcriptor Web Interface")

    # Ensure download directory exists
    success, download_info = ensure_download_directory()
    if success:
        print(f"[OK] Download directory: {download_info}")
    else:
        print(f"[WARNING] Could not setup download directory: {download_info}")

    print("Opening browser to http://localhost:8000")
    print("Press Ctrl+C to stop the server")

    # Create modified app
    app_instance = create_modified_app()

    # Open browser in a separate thread
    import threading
    browser_thread = threading.Thread(
        target=open_browser,
        args=("http://localhost:8000",),
        daemon=True
    )
    browser_thread.start()

    # Run server
    uvicorn.run(
        app_instance,
        host="127.0.0.1",
        port=8031,
        reload=False,
        log_level="info"
    )

if __name__ == "__main__":
    main()
