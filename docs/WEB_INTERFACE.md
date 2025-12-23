# Web Interface Documentation

This comprehensive documentation covers the YouTube Transcriptions GUI web interface, providing detailed information about setup, usage, architecture, and features of the web-based transcript extraction tool.

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Installation and Setup](#installation-and-setup)
- [Web Interface Features](#web-interface-features)
- [User Interface Guide](#user-interface-guide)
- [API Endpoints](#api-endpoints)
- [Template System](#template-system)
- [Italian Language Interface](#italian-language-interface)
- [Web vs CLI Comparison](#web-vs-cli-comparison)
- [Configuration and Customization](#configuration-and-customization)
- [Development and Testing](#development-and-testing)
- [Deployment Guide](#deployment-guide)
- [Troubleshooting](#troubleshooting)

## Overview

The YouTube Transcriptions GUI web interface provides a user-friendly, browser-based alternative to the CLI tool. Built with FastAPI and styled with Pico.css, it offers a clean, responsive design with real-time transcript preview and direct download capabilities.

### Key Features

- 🌐 **Browser-based Interface**: Accessible from any modern web browser
- 🎨 **Responsive Design**: Works seamlessly on desktop and mobile devices
- 📝 **Real-time Preview**: Instant transcript display after extraction
- 💾 **Direct Downloads**: Immediate file downloads in multiple formats
- 🌍 **Italian Language**: Native Italian interface for accessibility
- ⚡ **Fast Performance**: Rapid transcript extraction and rendering
- 🛡️ **Error Handling**: User-friendly error messages and guidance

## Quick Start

### Basic Usage

1. **Start the Web Server**
   ```bash
   uv run python -m src.web_app
   ```

2. **Open Browser**
   Navigate to `http://localhost:8000`

3. **Extract Transcript**
   - Enter YouTube URL
   - Select format (optional)
   - Choose language (optional)
   - Click "Estrai Trascrizione"

4. **Download Results**
   - Preview the transcript
   - Download in chosen format
   - Start new extraction

### Example Workflow

```
1. Open http://localhost:8000
2. Paste: https://www.youtube.com/watch?v=dQw4w9WgXcQ
3. Select "Sottotitoli SRT" format
4. Click "🚀 Estrai Trascrizione"
5. Preview results
6. Click "💾 Scarica SRT"
```

## Installation and Setup

### Prerequisites

- Python 3.13+
- uv package manager (recommended)
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Setup Process

1. **Clone Repository**
   ```bash
   git clone https://github.com/your-username/yt-transcriptor.git
   cd yt-transcriptor
   ```

2. **Install Dependencies**
   ```bash
   uv sync
   ```

3. **Verify Installation**
   ```bash
   uv run python -m pytest tests/
   ```

4. **Start Web Server**
   ```bash
   uv run python -m src.web_app
   ```

### Server Output

```
🚀 Starting YouTube Transcriptor Web Interface
📍 Open http://localhost:8000 in your browser
📖 Documentation: http://localhost:8000/docs
🛑 Press Ctrl+C to stop the server
```

## Web Interface Features

### 1. Homepage Interface

The homepage (`/`) provides:

- **Clean Form Design**: Minimal, distraction-free interface
- **URL Input Field**: Large, accessible input area for YouTube URLs
- **Format Selection**: Dropdown for TXT, SRT, VTT formats
- **Language Option**: Optional language code input
- **Usage Instructions**: Step-by-step guide
- **URL Examples**: Sample YouTube URL formats

### 2. Result Page

The result page (`/extract` results) displays:

- **Success Messages**: Confirmation of successful extraction
- **Video Information**: Title, URL, and metadata
- **Transcript Preview**: Scrollable content area
- **Download Options**: Format-specific download buttons
- **Statistics**: Line count, format, language info
- **Error Handling**: Detailed error messages with guidance

### 3. Download System

- **Direct Downloads**: Immediate file downloads via `/download/{filename}`
- **Temporary Storage**: Secure file handling with automatic cleanup
- **Format Preservation**: Downloads match selected format (TXT/SRT/VTT)
- **Filename Sanitization**: Safe, readable filenames based on video title

### 4. Error Management

- **Input Validation**: Real-time URL validation
- **API Error Handling**: Graceful handling of YouTube API issues
- **User Guidance**: Helpful error messages and suggestions
- **Recovery Options**: Easy retry mechanisms

## User Interface Guide

### Navigation Structure

```
Homepage (/)
├── Form Section
│   ├── URL Input
│   ├── Format Selection
│   └── Language Option
├── Instructions
│   ├── How-to Steps
│   └── URL Examples
└── Format Guide
    ├── TXT Description
    ├── SRT Description
    └── VTT Description
```

### Form Elements

#### URL Input Field
- **Type**: URL input with validation
- **Placeholder**: "https://www.youtube.com/watch?v=VIDEO_ID o https://youtu.be/VIDEO_ID"
- **Required**: Yes
- **Validation**: Real-time format checking

#### Format Selection
- **Options**:
  - `Testo Semplice (.txt)` - Default
  - `Sottotitoli SRT (.srt)`
  - `WebVTT (.vtt)`
- **Default**: TXT format

#### Language Input
- **Type**: Text input
- **Placeholder**: "es: it, en, es, fr"
- **Optional**: Yes
- **Behavior**: Auto-detect if empty

### Result Display

#### Success State
```
✅ Trascrizione estratta con successo!

📹 Informazioni Video
├── Titolo: [Video Title]
├── URL: [Video Link]
└── Stats:
    ├── [N] righe
    ├── [FORMAT] formato
    └── [LANG] lingua

📄 Trascrizione
[Scrollable content area]

💾 Scarica [FORMAT]  ← Nuova Estrazione
```

#### Error States
- **Invalid URL**: URL format validation error
- **No Transcript**: Video lacks transcript
- **Unexpected Error**: API or system issues

## API Endpoints

### Web Routes

#### GET `/`
- **Description**: Render homepage with extraction form
- **Response**: HTML page with form interface
- **Template**: `index.html`

#### POST `/extract`
- **Description**: Process transcript extraction request
- **Method**: Form POST with data
- **Parameters**:
  - `url` (required): YouTube video URL
  - `format_type` (optional): Output format (txt/srt/vtt)
  - `language` (optional): Language code
- **Response**: HTML page with results or error
- **Template**: `result.html`

#### GET `/download/{filename}`
- **Description**: Download transcript file
- **Parameter**: `filename` - Name of file to download
- **Response**: File download with appropriate MIME type
- **Security**: Temporary file validation

#### GET `/health`
- **Description**: Health check endpoint
- **Response**: JSON status
- **Example**: `{"status": "healthy", "service": "YouTube Transcriptor"}`

### Request/Response Formats

#### Extract Request (POST /extract)
```html
<form method="post" action="/extract">
    <input type="url" name="url" required>
    <select name="format_type">
        <option value="txt">Testo Semplice (.txt)</option>
        <option value="srt">Sottotitoli SRT (.srt)</option>
        <option value="vtt">WebVTT (.vtt)</option>
    </select>
    <input type="text" name="language" placeholder="it, en, es, fr">
    <button type="submit">Estrai Trascrizione</button>
</form>
```

#### Success Response Context
```python
{
    "request": request,
    "success": True,
    "video_title": "Video Title",
    "video_url": "https://youtube.com/watch?v=...",
    "transcript_content": "Formatted transcript text...",
    "format_type": "srt",
    "language": "it",
    "download_filename": "Video_Title_srt.txt",
    "lines_count": 150
}
```

#### Error Response Context
```python
{
    "request": request,
    "success": False,
    "error": "Error message description",
    "error_type": "invalid_url" | "no_transcript" | "unexpected"
}
```

## Template System

### Template Structure

```
src/templates/
├── base.html           # Base layout and styling
├── index.html          # Homepage with extraction form
└── result.html         # Results display page
```

### Base Template (base.html)

**Features:**
- **Responsive Design**: Mobile-first approach with CSS Grid
- **Pico.css Integration**: Minimal, clean CSS framework
- **Custom Styles**: Enhanced styling for specific components
- **Italian Language**: Native Italian text throughout
- **Accessibility**: Semantic HTML and ARIA labels

**Key Components:**
- HTML5 semantic structure
- Responsive viewport meta tags
- Pico.css CDN integration
- Custom CSS for layout and components
- Footer with navigation links

### Homepage Template (index.html)

**Sections:**
1. **Extraction Form**: Main interface for user input
2. **Instructions**: Step-by-step usage guide
3. **URL Examples**: Format examples and validation
4. **Format Guide**: Description of available output formats

**Form Features:**
- Required URL field with HTML5 validation
- Format selection dropdown
- Optional language input
- Submit button with emoji icon

### Result Template (result.html)

**Dynamic Content:**
- **Success/Error State**: Conditional rendering based on extraction result
- **Video Information**: Metadata display with statistics
- **Transcript Preview**: Scrollable content area
- **Download Actions**: Format-specific download buttons

**Error Handling:**
- Specific error messages for different failure types
- Helpful guidance and suggestions
- Recovery options and retry mechanisms

### Custom CSS Components

#### Form Container
```css
.form-container {
    background: var(--card-background-color, #fff);
    border-radius: var(--border-radius, 0.25rem);
    padding: 1.5rem;
    margin-bottom: 2rem;
}
```

#### Transcript Display
```css
.transcript-content {
    background: var(--code-background-color, #f8f9fa);
    border-radius: var(--border-radius, 0.25rem);
    padding: 1rem;
    font-family: var(--font-family, monospace);
    white-space: pre-wrap;
    max-height: 400px;
    overflow-y: auto;
}
```

#### Message Styling
```css
.success-message, .error-message {
    border-radius: var(--border-radius, 0.25rem);
    padding: 1rem;
    margin: 1rem 0;
}
```

## Italian Language Interface

### Language Choice Rationale

The web interface is implemented in Italian to:
- **Enhance Accessibility**: Native language for Italian-speaking users
- **Improve User Experience**: Natural, comfortable interaction
- **Demonstrate Localization**: Showcase internationalization capabilities
- **Cultural Consideration**: Respect for local user preferences

### Interface Text

#### Navigation and Actions
- "Estrai Trascrizione" - Extract Transcript
- "Nuova Estrazione" - New Extraction
- "Scarica [FORMAT]" - Download [FORMAT]
- "Riprova" - Try Again

#### Form Labels
- "URL del Video YouTube" - YouTube Video URL
- "Formato Output" - Output Format
- "Codice Lingua (opzionale)" - Language Code (optional)
- "Testo Semplice (.txt)" - Plain Text (.txt)
- "Sottotitoli SRT (.srt)" - SRT Subtitles (.srt)
- "WebVTT (.vtt)" - WebVTT (.vtt)

#### Success Messages
- "Trascrizione estratta con successo!" - Transcript extracted successfully!
- "Informazioni Video" - Video Information
- "righe" - lines
- "formato" - format
- "lingua" - language

#### Error Messages
- "Si è verificato un errore" - An error occurred
- "URL non valido" - Invalid URL
- "Trascrizione non disponibile" - Transcript not available
- "Errore imprevisto" - Unexpected error

#### Help Text
- "Come Funziona" - How It Works
- "Esempi di URL" - URL Examples
- "Formati Disponibili" - Available Formats
- "Suggerimenti" - Tips

### Localization Considerations

#### Future Enhancements
- **Multi-language Support**: Template system ready for internationalization
- **Language Detection**: Automatic language preference detection
- **Translation Files**: External translation file management
- **RTL Support**: Right-to-left language compatibility

#### Implementation Strategy
```python
# Future localization structure
locales/
├── it.json          # Italian translations
├── en.json          # English translations
└── es.json          # Spanish translations
```

## Web vs CLI Comparison

### Feature Comparison

| Feature | Web Interface | CLI Interface |
|---------|---------------|---------------|
| **Ease of Use** | ⭐⭐⭐⭐⭐ Very user-friendly | ⭐⭐⭐ Requires technical knowledge |
| **Speed** | ⭐⭐⭐⭐ Fast with preview | ⭐⭐⭐⭐⭐ Fastest execution |
| **Flexibility** | ⭐⭐⭐ Limited to web features | ⭐⭐⭐⭐⭐ Full parameter control |
| **Integration** | ⭐⭐ Browser-based only | ⭐⭐⭐⭐⭐ Scriptable/automatable |
| **Accessibility** | ⭐⭐⭐⭐⭐ Visual, intuitive | ⭐⭐ Command-line only |
| **Mobile Support** | ⭐⭐⭐⭐⭐ Fully responsive | ⭐⭐ Limited (terminal apps) |
| **Batch Processing** | ❌ Not supported | ⭐⭐⭐⭐⭐ Scriptable |
| **File Management** | ⭐⭐⭐ Direct downloads | ⭐⭐⭐⭐⭐ Full control |

### Use Case Recommendations

#### Use Web Interface When:
- **Non-technical users** need transcript extraction
- **Quick one-off extractions** are required
- **Visual preview** of content is helpful
- **Mobile access** is needed
- **Simple workflow** is preferred
- **No scripting/automation** requirements

#### Use CLI Interface When:
- **Technical users** prefer command-line tools
- **Batch processing** of multiple videos
- **Automation and scripting** are needed
- **Custom workflows** are required
- **Integration** with other tools
- **Advanced parameters** and configuration

### Migration Between Interfaces

Both interfaces use the same core functionality:

```python
# Shared core modules
from .transcriptor import get_transcript, get_video_title
from .file_handler import format_transcript, save_transcript
from .utils import validate_youtube_url
```

**Data Consistency**: Both interfaces produce identical output formats and use the same validation and extraction logic.

## Configuration and Customization

### Server Configuration

#### Default Settings
```python
# Server configuration
HOST = "127.0.0.1"
PORT = 8000
DEBUG = True  # For development
RELOAD = True  # Auto-reload on code changes
```

#### Custom Configuration
```python
# Environment variables
import os
HOST = os.getenv("YT_HOST", "127.0.0.1")
PORT = int(os.getenv("YT_PORT", "8000"))
DEBUG = os.getenv("YT_DEBUG", "false").lower() == "true"
```

### Customization Options

#### Styling Customization
```css
/* Custom CSS additions */
.container {
    max-width: 1000px; /* Wider layout */
}

.form-container {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}
```

#### Template Customization
```html
<!-- Adding custom logo -->
<header class="header">
    <img src="/static/logo.png" alt="Logo" style="height: 50px;">
    <hgroup>
        <h1>🎬 YouTube Transcriptor</h1>
    </hgroup>
</header>
```

#### Feature Extensions
```python
# Custom endpoint example
@app.get("/stats")
async def get_stats():
    """Return usage statistics."""
    return {
        "extractions_today": 42,
        "total_extractions": 1337,
        "popular_formats": ["txt", "srt", "vtt"]
    }
```

### Environment Variables

```bash
# Production configuration
export YT_HOST=0.0.0.0
export YT_PORT=8080
export YT_DEBUG=false
export YT_SECRET_KEY="your-secret-key"
```

## Development and Testing

### Development Setup

1. **Install Development Dependencies**
   ```bash
   uv sync --extra dev
   ```

2. **Run Development Server**
   ```bash
   uv run python -m src.web_app
   ```

3. **Enable Auto-reload**
   ```bash
   uv run uvicorn src.web_app:app --reload --host 0.0.0.0 --port 8000
   ```

### Testing the Web Interface

#### 1. Unit Testing
```python
# tests/test_web_app.py
import pytest
from fastapi.testclient import TestClient
from src.web_app import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_index_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "YouTube Transcriptor" in response.text
```

#### 2. Integration Testing
```python
def test_extract_endpoint():
    response = client.post("/extract", data={
        "url": "https://www.youtube.com/watch?v=test123",
        "format_type": "txt",
        "language": "en"
    })
    assert response.status_code == 200
    assert "Trascrizione" in response.text or "Errore" in response.text
```

#### 3. End-to-End Testing
```python
def test_full_workflow():
    # Test homepage loads
    response = client.get("/")
    assert response.status_code == 200

    # Test form submission
    response = client.post("/extract", data={
        "url": "https://youtu.be/dQw4w9WgXcQ",
        "format_type": "srt"
    })
    assert response.status_code == 200
```

### Testing Dependencies

```toml
# pyproject.toml development dependencies
[project.optional-dependencies]
dev = [
    "coverage>=7.12.0",
    "pytest>=9.0.1",
    "httpx>=0.28.1",          # For TestClient
    "pytest-mock>=3.15.1",
    "jinja2>=3.1.6",          # Template testing
    "aiofiles>=23.0.0",       # Async file operations
]
```

### Running Web Tests

```bash
# Run web-specific tests
uv run python -m pytest tests/test_web_app.py

# Run with coverage
uv run python -m pytest tests/test_web_app.py --cov=src.web_app

# Run all tests including web
uv run python -m pytest tests/
```

### Browser Testing

#### Manual Testing Checklist
- [ ] Homepage loads correctly
- [ ] Form validation works
- [ ] Transcript extraction succeeds
- [ ] Error handling displays correctly
- [ ] File downloads work
- [ ] Responsive design on mobile
- [ ] Different browsers compatibility

#### Automated Browser Testing
```python
# Using pytest-playwright for browser automation
import pytest
from playwright.sync_api import Page

def test_user_workflow(page: Page):
    page.goto("http://localhost:8000")

    # Fill form
    page.fill("input[name='url']", "https://youtu.be/test123")
    page.select_option("select[name='format_type']", "srt")

    # Submit form
    page.click("button[type='submit']")

    # Verify result
    page.wait_for_selector(".transcript-content")
    assert "Trascrizione" in page.content()
```

## Deployment Guide

### Production Deployment

#### 1. Server Requirements
- **Python 3.13+**: Runtime environment
- **Reverse Proxy**: Nginx or Apache
- **Process Manager**: Gunicorn or uWSGI
- **SSL Certificate**: HTTPS configuration

#### 2. Gunicorn Configuration
```bash
# Install Gunicorn
pip install gunicorn

# Start with Gunicorn
gunicorn src.web_app:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
```

#### 3. Nginx Configuration
```nginx
# /etc/nginx/sites-available/yt-transcriptor
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### 4. SSL Configuration
```bash
# Let's Encrypt SSL
sudo certbot --nginx -d your-domain.com
```

### Docker Deployment

#### Dockerfile
```dockerfile
FROM python:3.13-slim

WORKDIR /app

# Copy dependencies
COPY pyproject.toml .
RUN pip install uv && uv sync --frozen

# Copy application
COPY src/ ./src/

# Expose port
EXPOSE 8000

# Start application
CMD ["uv", "run", "uvicorn", "src.web_app:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  yt-transcriptor:
    build: .
    ports:
      - "8000:8000"
    environment:
      - YT_HOST=0.0.0.0
      - YT_PORT=8000
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/ssl
    depends_on:
      - yt-transcriptor
```

### Cloud Deployment

#### Heroku
```bash
# Procfile
web: uv run uvicorn src.web_app:app --host 0.0.0.0 --port $PORT

# Deploy
git add .
git commit -m "Deploy web interface"
git push heroku main
```

#### Railway/Render
- **Automatic Deployment**: Connect Git repository
- **Environment Variables**: Configure via dashboard
- **SSL**: Automatically provided
- **Scaling**: Easy horizontal scaling

### Monitoring and Logging

#### Application Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.post("/extract")
async def extract_transcript(request: Request, ...):
    logger.info(f"Extraction request: {url}")
    # ... processing
    logger.info(f"Extraction completed: {success}")
```

#### Health Monitoring
```python
@app.get("/health")
async def health_check():
    """Enhanced health check."""
    try:
        # Test core functionality
        test_url = "https://www.youtube.com/watch?v=test"
        validate_youtube_url(test_url)

        return {
            "status": "healthy",
            "service": "YouTube Transcriptor",
            "version": "1.0.0",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }
```

## Troubleshooting

### Common Issues

#### 1. Server Won't Start
**Problem**: Address already in use
```bash
# Solution
lsof -ti:8000 | xargs kill -9
# Or use different port
uv run python -m src.web_app --port 8001
```

#### 2. Templates Not Found
**Problem**: Template directory not found
```python
# Solution in web_app.py
templates = Jinja2Templates(directory="src/templates")
```

#### 3. Static Files Not Loading
**Problem**: 404 errors for CSS/JS
```python
# Solution: Mount static files
app.mount("/static", StaticFiles(directory="src/static"), name="static")
```

#### 4. CORS Issues
**Problem**: Cross-origin requests blocked
```python
# Solution: Add CORS middleware
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(CORSMiddleware, allow_origins=["*"])
```

### Debug Mode

#### Enable Debug Logging
```python
import uvicorn
uvicorn.run(
    "web_app:app",
    host="127.0.0.1",
    port=8000,
    reload=True,
    log_level="debug"
)
```

#### Browser Developer Tools
- **Network Tab**: Monitor API requests
- **Console**: Check JavaScript errors
- **Elements**: Inspect HTML/CSS

### Performance Issues

#### Slow Loading Times
```python
# Solution: Add caching
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

FastAPICache.init(InMemoryBackend())
```

#### Memory Usage
```python
# Solution: Cleanup temporary files
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    # Cleanup on shutdown
    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR, ignore_errors=True)
```

### Security Considerations

#### File Upload Security
```python
# Solution: Validate file paths
def safe_path_join(base_dir: Path, filename: str) -> Path:
    """Safely join paths to prevent directory traversal."""
    return (base_dir / filename).resolve()
```

#### Rate Limiting
```python
# Solution: Add rate limiting
from fastapi import FastAPI, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/extract")
@limiter.limit("10/minute")
async def extract_transcript(request: Request, ...):
    # ... implementation
```

---

**Conclusion**: The YouTube Transcriptor web interface provides a user-friendly, browser-based alternative to the CLI tool, featuring a clean Italian-language interface with real-time transcript preview and direct download capabilities. Built on FastAPI with responsive Pico.css styling, it offers an accessible solution for users who prefer graphical interfaces while maintaining the same powerful core functionality as the CLI version.

For additional information:
- See [API Documentation](API.md) for detailed endpoint specifications
- Review [Architecture Guide](ARCHITECTURE.md) for system design details
- Consult [Development Guide](DEVELOPMENT.md) for setup and customization
- Check [CLI Documentation](../README.md) for command-line usage