# Development Guide

This comprehensive guide provides everything developers need to know to work with the YouTube Transcriptor project.

## Table of Contents

- [Development Environment Setup](#development-environment-setup)
- [Project Structure](#project-structure)
- [Coding Standards](#coding-standards)
- [Testing Strategy](#testing-strategy)
- [Debugging Guide](#debugging-guide)
- [Performance Optimization](#performance-optimization)
- [Release Process](#release-process)
- [Troubleshooting](#troubleshooting)

## Development Environment Setup

### Prerequisites

- **Python 3.13+**: Required for modern language features
- **uv**: Fast Python package manager (recommended)
- **Git**: Version control system
- **IDE/Editor**: VS Code, PyCharm, or similar (recommended)
- **Modern Web Browser**: Chrome, Firefox, Safari, or Edge for web interface testing

### Initial Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/yt-transcriptor.git
   cd yt-transcriptor
   ```

2. **Set up Python environment**
   ```bash
   # Using uv (recommended)
   uv sync

   # Or using venv
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev]"
   ```

3. **Verify installation**
   ```bash
   uv run python -m pytest tests/
   uv run python -m src.main --help
   ```

4. **Test web interface (optional)**
   ```bash
   uv run python -m src.web_app
   # Open http://localhost:8000 in browser
   ```

### IDE Configuration

#### VS Code Setup

1. **Install extensions**
   - Python
   - Pylance
   - Python Docstring Generator
   - GitLens

2. **Configure settings**
   ```json
   {
       "python.defaultInterpreterPath": ".venv/bin/python",
       "python.formatting.provider": "black",
       "python.linting.enabled": true,
       "python.linting.pylintEnabled": true,
       "python.testing.pytestEnabled": true,
       "python.testing.unittestEnabled": false
   }
   ```

3. **Create workspace settings** (`.vscode/settings.json`)

#### PyCharm Setup

1. **Configure Python interpreter**
   - Settings → Project → Python Interpreter
   - Add new interpreter using uv or venv

2. **Enable pytest integration**
   - Settings → Tools → Python Integrated Tools
   - Testing → Default test runner: pytest

3. **Configure code style**
   - Settings → Editor → Code Style → Python
   - Import PEP 8 settings

## Project Structure

### Directory Layout

```
yt-transcriptor/
├── src/                     # Source code
│   ├── __init__.py         # Package initialization
│   ├── main.py             # CLI interface and orchestration
│   ├── transcriptor.py     # Core transcript extraction logic
│   ├── file_handler.py     # File operations and formatting
│   ├── utils.py            # Utility functions
│   ├── web_app.py          # FastAPI web interface
│   ├── templates/          # HTML templates for web interface
│   │   ├── base.html       # Base layout template
│   │   ├── index.html      # Homepage with extraction form
│   │   └── result.html     # Results display template
│   └── static/             # Static files (CSS, JS, images)
│       ├── css/            # Custom stylesheets
│       ├── js/             # JavaScript files
│       └── images/         # Image assets
├── tests/                  # Test suite
│   ├── __init__.py         # Test package initialization
│   ├── test_main.py        # CLI interface tests
│   ├── test_transcriptor.py # Core logic tests
│   ├── test_file_handler.py # File operations tests
│   ├── test_utils.py       # Utility function tests
│   ├── test_web_app.py     # Web interface tests
│   ├── test_integration.py # End-to-end tests
│   └── test_project_setup.py # Environment setup tests
├── docs/                   # Documentation
│   ├── API.md              # API documentation
│   ├── ARCHITECTURE.md     # System architecture
│   ├── CONTRIBUTING.md     # Contribution guidelines
│   ├── DEVELOPMENT.md      # Development guide
│   ├── WEB_INTERFACE.md    # Web interface documentation
│   └── CHANGELOG.md        # Version history
├── htmlcov/               # Coverage reports (generated)
├── transcriptions/        # Default output directory
├── .gitignore            # Git ignore rules
├── pyproject.toml        # Project configuration
├── uv.lock              # Dependency lock file
├── README.md            # Project overview
└── CLAUDE.md            # Project requirements
```

### Module Responsibilities

#### src/main.py
- Command-line interface
- Argument parsing and validation
- User interaction and feedback
- Workflow orchestration

#### src/transcriptor.py
- YouTube API integration
- Transcript extraction
- Video metadata retrieval
- Error handling for API operations

#### src/file_handler.py
- File system operations
- Transcript formatting (TXT, SRT, VTT)
- Filename sanitization
- Output directory management

#### src/utils.py
- URL validation
- Text processing and sanitization
- Common utility functions

#### src/web_app.py
- FastAPI web application framework
- HTTP request/response handling
- HTML template rendering with Jinja2
- Form processing and validation
- File download management
- Temporary file handling and cleanup

#### src/templates/
HTML templates for web interface with Italian language support:
- **base.html**: Base layout with Pico.css styling and navigation
- **index.html**: Homepage with extraction form and instructions
- **result.html**: Results display with transcript preview and download options

#### src/static/
Static assets for web interface:
- **css/**: Custom stylesheets extending Pico.css
- **js/**: JavaScript files for enhanced functionality
- **images/**: Image assets and icons

## Coding Standards

### Code Style

Follow [PEP 8](https://pep8.org/) with these additional conventions:

1. **Line Length**: 88 characters (Black standard)
2. **Imports**: Group and organize imports properly
3. **Naming**: Use descriptive names following conventions
4. **Comments**: Explain "why", not "what"

### Example Code Style

```python
"""Module docstring following Google style.

This module provides functionality for YouTube transcript extraction.
"""

from pathlib import Path
from typing import Dict, List, Optional

from .utils import validate_youtube_url


def extract_transcript(
    video_url: str,
    language: Optional[str] = None
) -> List[Dict[str, any]]:
    """Extract transcript from YouTube video.

    Args:
        video_url: YouTube video URL to extract transcript from
        language: Optional language code for transcript preference

    Returns:
        List of transcript entries with text, start time, and duration

    Raises:
        InvalidVideoURLError: If the URL is not a valid YouTube URL
        NoTranscriptAvailableError: If no transcript is available
    """
    if not validate_youtube_url(video_url):
        raise InvalidVideoURLError(f"Invalid URL: {video_url}")

    # Implementation here
    pass
```

### Type Hints

Use type hints for all function signatures and important variables:

```python
from typing import Dict, List, Optional, Union

def process_transcript(
    transcript_data: List[Dict[str, Union[str, float]]],
    format_type: str
) -> str:
    """Process transcript data into specified format."""
    pass
```

### Error Handling

Follow consistent error handling patterns:

```python
def safe_operation():
    """Example of proper error handling."""
    try:
        result = risky_operation()
        return result
    except SpecificError as e:
        logger.warning(f"Expected error occurred: {e}")
        return default_value
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise
```

## Web Development Patterns

### FastAPI Development

#### Application Structure
```python
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(title="YouTube Transcriptor")
templates = Jinja2Templates(directory="src/templates")
```

#### Route Definitions
```python
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render homepage with form."""
    return templates.TemplateResponse(request, "index.html")

@app.post("/extract", response_class=HTMLResponse)
async def extract_transcript(
    request: Request,
    url: str = Form(...),
    format_type: str = Form(default="txt")
):
    """Process transcript extraction."""
    # Processing logic
    return templates.TemplateResponse(request, "result.html", context)
```

#### Form Handling
```python
# Form validation and processing
async def process_form_data(request: Request):
    """Process and validate form submission."""
    form = await request.form()
    url = form.get("url")
    format_type = form.get("format_type", "txt")

    # Validation
    if not validate_youtube_url(url):
        raise InvalidVideoURLError("Invalid YouTube URL")

    return url, format_type
```

### Template Development

#### Jinja2 Template Structure
```html
{% extends "base.html" %}

{% block title %}Custom Page Title{% endblock %}

{% block content %}
<div class="container">
    {% if success %}
        <div class="success-message">
            ✅ Operation completed successfully!
        </div>
    {% else %}
        <div class="error-message">
            ❌ An error occurred: {{ error }}
        </div>
    {% endif %}
</div>
{% endblock %}
```

#### Template Inheritance
```html
<!-- base.html -->
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}YouTube Transcriptor{% endblock %}</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@1/css/pico.min.css">
    <style>
        /* Custom styles */
        .container { max-width: 800px; margin: 0 auto; }
    </style>
</head>
<body>
    <main class="container">
        <header>
            <h1>🎬 YouTube Transcriptor</h1>
        </header>

        {% block content %}{% endblock %}

        <footer>
            <hr>
            <p><small>YouTube Transcriptor</small></p>
        </footer>
    </main>
</body>
</html>
```

### HTML/CSS Best Practices

#### Responsive Design
```css
/* Mobile-first responsive design */
.container {
    max-width: 800px;
    margin: 0 auto;
    padding: 1rem;
}

@media (max-width: 768px) {
    .container {
        padding: 0.5rem;
    }

    .download-section {
        flex-direction: column;
    }
}
```

#### Form Styling
```css
.form-group {
    margin-bottom: 1rem;
}

.form-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 600;
}

.transcript-content {
    background: var(--code-background-color, #f8f9fa);
    border-radius: var(--border-radius, 0.25rem);
    padding: 1rem;
    font-family: monospace;
    white-space: pre-wrap;
    max-height: 400px;
    overflow-y: auto;
}
```

### Web-Specific Testing

#### FastAPI Test Client
```python
from fastapi.testclient import TestClient
from src.web_app import app

client = TestClient(app)

def test_web_interface():
    """Test web interface endpoints."""
    # Test homepage
    response = client.get("/")
    assert response.status_code == 200
    assert "YouTube Transcriptor" in response.text

    # Test form submission
    response = client.post("/extract", data={
        "url": "https://www.youtube.com/watch?v=test123",
        "format_type": "txt"
    })
    assert response.status_code == 200
```

#### Template Testing
```python
def test_template_rendering():
    """Test template context rendering."""
    from fastapi.templating import Jinja2Templates

    templates = Jinja2Templates(directory="src/templates")

    # Mock request object
    class MockRequest:
        def __init__(self):
            self.base_url = "http://localhost:8000"

    request = MockRequest()
    context = {"success": True, "video_title": "Test Video"}

    # Test template rendering
    response = templates.TemplateResponse(request, "result.html", context)
    assert "Test Video" in response.body.decode()
```

### Web Development Workflow

#### Development Server
```bash
# Start development server with auto-reload
uv run uvicorn src.web_app:app --reload --host 0.0.0.0 --port 8000

# Start with debug logging
uv run uvicorn src.web_app:app --reload --log-level debug
```

#### Browser Testing Checklist
- [ ] Test all workflows in multiple browsers (Chrome, Firefox, Safari, Edge)
- [ ] Verify responsive design on mobile and desktop
- [ ] Test form validation and error handling
- [ ] Verify file download functionality
- [ ] Test accessibility features (keyboard navigation, screen readers)
- [ ] Check Italian language display and formatting

#### Debugging Web Applications
```python
# Enable debug mode
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "web_app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="debug"
    )
```

#### Performance Monitoring
```python
# Add request timing middleware
import time
from fastapi import Request

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

## Testing Strategy

### Test Categories

#### 1. Unit Tests
- Test individual functions in isolation
- Mock external dependencies
- Fast execution and focused scope

```python
def test_validate_youtube_url_valid():
    """Test URL validation with valid URLs."""
    from src.utils import validate_youtube_url

    valid_urls = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://youtu.be/dQw4w9WgXcQ"
    ]

    for url in valid_urls:
        assert validate_youtube_url(url) is True
```

#### 2. Integration Tests
- Test component interactions
- Use real dependencies where appropriate
- Verify end-to-end workflows

```python
def test_full_workflow():
    """Test complete transcript extraction workflow."""
    with patch('src.transcriptor.YouTubeTranscriptApi') as mock_api:
        mock_transcript = [
            {'text': 'Hello world', 'start': 0.0, 'duration': 2.5}
        ]
        mock_api.get_transcript.return_value = mock_transcript

        result = get_transcript("https://youtu.be/test123")
        assert result == mock_transcript
```

#### 3. CLI Tests
- Test command-line interface
- Verify argument parsing
- Test user interaction

```python
def test_cli_argument_parsing():
    """Test CLI argument parsing."""
    from src.main import parse_arguments

    args = parse_arguments(["https://youtu.be/test123", "--format", "srt"])
    assert args.url == "https://youtu.be/test123"
    assert args.format == "srt"
```

### Testing Best Practices

#### 1. Use Fixtures
```python
import pytest

@pytest.fixture
def sample_transcript():
    """Provide sample transcript data for tests."""
    return [
        {'text': 'Hello world', 'start': 0.0, 'duration': 2.5},
        {'text': 'This is a test', 'start': 2.5, 'duration': 3.0}
    ]

def test_format_transcript(sample_transcript):
    """Test transcript formatting with sample data."""
    result = format_transcript(sample_transcript, "txt")
    assert "Hello world" in result
```

#### 2. Mock External Dependencies
```python
from unittest.mock import patch, MagicMock

def test_api_integration():
    """Test API integration with mocking."""
    with patch('src.transcriptor.YouTubeTranscriptApi') as mock_api:
        mock_api.return_value.get_transcript.return_value = []

        result = get_transcript("https://youtu.be/test123")

        mock_api.assert_called_once()
        assert isinstance(result, list)
```

#### 3. Test Error Cases
```python
def test_invalid_url_handling():
    """Test error handling for invalid URLs."""
    with pytest.raises(InvalidVideoURLError):
        get_transcript("invalid-url")
```

### Running Tests

```bash
# Run all tests
uv run python -m pytest tests/

# Run with coverage
uv run python -m pytest tests/ --cov=src --cov-report=html

# Run specific test file
uv run python -m pytest tests/test_utils.py

# Run with verbose output
uv run python -m pytest tests/ -v

# Run specific test function
uv run python -m pytest tests/test_utils.py::test_validate_youtube_url
```

### Coverage Goals

- **Target**: 95%+ code coverage
- **Critical**: 100% coverage for core business logic
- **Minimum**: 90% coverage for all modules

## Debugging Guide

### Common Issues

#### 1. Import Errors
```python
# Problem: ModuleNotFoundError
# Solution: Check PYTHONPATH and package installation
import sys
sys.path.append(str(Path(__file__).parent.parent))
```

#### 2. Mocking Issues
```python
# Problem: Mock not applied correctly
# Solution: Patch where the object is used, not where it's defined
with patch('src.transcriptor.YouTubeTranscriptApi') as mock_api:  # Correct
    # NOT: with patch('youtube_transcript_api.YouTubeTranscriptApi')
```

#### 3. Path Issues
```python
# Problem: File not found errors
# Solution: Use pathlib for cross-platform compatibility
from pathlib import Path

config_path = Path(__file__).parent / "config.json"
```

### Debugging Tools

#### 1. pdb (Python Debugger)
```python
import pdb

def debug_function():
    pdb.set_trace()  # Execution stops here
    # Debug your code
    pass
```

#### 2. Logging
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def debug_function():
    logger.debug("Starting function")
    logger.info("Processing data")
    logger.warning("Potential issue detected")
```

#### 3. pytest Debugging
```bash
# Stop on first failure
uv run python -m pytest tests/ -x

# Show local variables on failure
uv run python -m pytest tests/ -l

# Drop into pdb on failure
uv run python -m pytest tests/ --pdb
```

## Performance Optimization

### Profiling

#### 1. Line Profiler
```python
pip install line_profiler

@profile
def slow_function():
    # Function to profile
    pass

# Run with:
kernprof -l -v script.py
```

#### 2. Memory Profiling
```python
pip install memory_profiler

@profile
def memory_intensive_function():
    # Function to profile
    pass

# Run with:
python -m memory_profiler script.py
```

### Optimization Techniques

#### 1. Efficient String Operations
```python
# Bad: Repeated string concatenation
result = ""
for item in items:
    result += str(item) + ","

# Good: Join operation
result = ",".join(str(item) for item in items)
```

#### 2. Context Managers
```python
# Always use context managers for file operations
with open("file.txt", "r") as f:
    content = f.read()
```

#### 3. List Comprehensions
```python
# Good: List comprehension
squares = [x**2 for x in range(10)]

# Avoid: Unnecessary loops
squares = []
for x in range(10):
    squares.append(x**2)
```

## Building Windows Executables

### Prerequisites

- Windows operating system
- Python 3.13+ with uv package manager
- Packaging dependencies: `uv sync --extra packaging`

### Build Process

#### Using Makefile (Recommended)

```bash
# Build both executables
make build-all-exe

# Build CLI executable only
make build-cli-exe

# Build web executable only
make build-web-exe

# Test executables
make test-exe
```

#### Manual Build with PyInstaller

```bash
# Install packaging dependencies
uv sync --extra packaging

# Build CLI executable
uv run pyinstaller --onefile --console \
  --name "yt-transcriptor-cli" \
  src/cli_main.py

# Build Web executable
uv run pyinstaller --onefile --windowed \
  --add-data "src/templates;templates" \
  --add-data "src/static;static" \
  --name "yt-transcriptor-web" \
  src/web_main.py
```

### Executable Specifications

#### CLI Executable (yt-transcriptor-cli.exe)
- **Entry Point**: `src/cli_main.py`
- **Type**: Console application
- **PyInstaller Options**: `--onefile --console`
- **Target**: Command-line users and automation

#### Web Executable (yt-transcriptor-web.exe)
- **Entry Point**: `src/web_main.py`
- **Type**: Windowed application
- **PyInstaller Options**: `--onefile --windowed`
- **Data Files**: Templates and static assets
- **Target**: Everyday users with browser interface

### Build Output

After building, executables will be located in:
- `dist/yt-transcriptor-cli.exe` - CLI executable
- `dist/yt-transcriptor-web.exe` - Web executable

### Testing Executables

```bash
# Test CLI executable
dist/yt-transcriptor-cli.exe --help
dist/yt-transcriptor-cli.exe "https://www.youtube.com/watch?v=VIDEO_ID"

# Test web executable (manual process)
# 1. Run dist/yt-transcriptor-web.exe
# 2. Verify browser opens to http://localhost:8000
# 3. Test transcript extraction through web interface
# 4. Verify files saved to ~/yt-transcriptions/
```

### Distribution Considerations

#### File Sizes
- CLI executable: ~15-20 MB
- Web executable: ~25-30 MB (includes templates/assets)

#### Dependencies
- Both executables are self-contained
- No Python installation required on target machines
- All dependencies bundled using PyInstaller

#### Platform Compatibility
- Currently Windows-specific
- Linux/Mac builds can be added with additional PyInstaller configurations
- Web executable may need platform-specific adjustments

### Troubleshooting Builds

#### Common Issues

1. **Missing Data Files**
   ```bash
   # Ensure templates and static directories are included
   --add-data "src/templates;templates" \
   --add-data "src/static;static"
   ```

2. **Import Errors**
   ```bash
   # Use explicit hidden imports
   --hidden-import=transcriptor \
   --hidden-import=file_handler \
   --hidden-import=utils
   ```

3. **Permission Issues**
   ```bash
   # Run as administrator on Windows if needed
   # or adjust User Account Control settings
   ```

#### Debug Builds

```bash
# Create debug build for troubleshooting
uv run pyinstaller --onefile --console --debug all \
  --name "yt-transcriptor-cli-debug" \
  src/cli_main.py
```

## Release Process

### Version Management

Use semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

#### 1. Pre-release
```bash
# Run full test suite
uv run python -m pytest tests/ --cov=src

# Check code style
black src/ tests/
flake8 src/ tests/

# Update documentation
# Update version in pyproject.toml
# Update CHANGELOG.md

# Test build process
make clean
make build-all-exe
```

#### 2. Testing
```bash
# Test installation
pip install -e .
python -m src.cli_main --help
python -m src.web_main  # Test web interface

# Test CLI scripts
yt-transcriptor-cli --help

# Test executables
make test-exe
```

#### 3. Release
```bash
# Tag release
git tag -a v0.1.0 -m "Release version 0.1.0"
git push origin v0.1.0

# Build package
python -m build

# Build executables
make build-all-exe

# Upload to PyPI (if applicable)
python -m twine upload dist/*

# Create GitHub Release with executables
# Attach dist/*.exe files to release assets
```

## Troubleshooting

### Common Development Issues

#### 1. Dependency Issues
```bash
# Problem: Package conflicts
# Solution: Recreate environment
rm -rf .venv
uv sync

# Or use pip directly
pip install --force-reinstall -e ".[dev]"
```

#### 2. Test Failures
```bash
# Problem: Tests failing unexpectedly
# Solution: Check test isolation
uv run python -m pytest tests/ --reuse-db

# Clear test cache
find . -name "*.pyc" -delete
find . -name "__pycache__" -delete
```

#### 3. Import Path Issues
```python
# Problem: Relative import failures
# Solution: Use absolute imports
from src.transcriptor import get_transcript  # Good
from .transcriptor import get_transcript    # Also good for same package
```

### Environment Issues

#### 1. Python Version Mismatch
```bash
# Check Python version
python --version

# Use uv to manage versions
uv python pin 3.13
```

#### 2. Platform-specific Issues
```python
# Use pathlib for cross-platform compatibility
from pathlib import Path

config_file = Path.home() / ".config" / "app" / "config.json"
```

### Getting Help

1. **Check logs**: Look for detailed error messages
2. **Review documentation**: Check API docs and architecture guide
3. **Search issues**: Look for similar problems in GitHub issues
4. **Ask questions**: Use GitHub discussions for help

### Performance Monitoring

```python
# Monitor function performance
import time
import functools

def timing_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.2f} seconds")
        return result
    return wrapper

@timing_decorator
def slow_function():
    time.sleep(1)
    return "done"
```

This development guide provides comprehensive coverage of the development process, from setup to deployment. Regular updates and additions to this document will help maintain consistency and quality across the development team.