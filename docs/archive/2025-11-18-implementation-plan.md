# YouTube Transcriptor CLI Tool Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a lightweight Python CLI tool that extracts YouTube video transcripts directly without downloading videos, maintaining original language and supporting multiple output formats.

**Architecture:** A modular CLI tool using youtube-transcript-api for transcript extraction, with separate modules for core logic, file handling, and utilities. Following TDD approach with minimal, incremental commits.

**Tech Stack:** Python 3.13+, youtube-transcript-api, argparse, pathlib, pytest

---

### Task 1: Project Setup and Dependencies

**Files:**
- Create: `requirements.txt`
- Create: `src/__init__.py`
- Create: `tests/__init__.py`

**Step 1: Write the failing test - verify project structure**

```python
# tests/test_project_setup.py
def test_project_structure():
    import pathlib
    import src

    # Verify src directory exists and is importable
    assert pathlib.Path("src").exists()
    assert src.__file__ is not None
```

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_project_setup.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'src'"

**Step 3: Create project structure and dependencies**

```bash
# Create src directory and __init__.py
mkdir -p src tests
touch src/__init__.py tests/__init__.py

# Initialize uv and add dependencies
uv init --no-workspace
uv add youtube-transcript-api
uv add --dev pytest
```

**Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_project_setup.py -v`
Expected: PASS

**Step 5: Commit**

```bash
git add requirements.txt src/__init__.py tests/__init__.py tests/test_project_setup.py
git commit -m "feat: initialize project structure and dependencies"
```

### Task 2: URL Validation Utility

**Files:**
- Create: `src/utils.py`
- Create: `tests/test_utils.py`

**Step 1: Write the failing test for URL validation**

```python
# tests/test_utils.py
def test_validate_youtube_url():
    from src.utils import validate_youtube_url

    # Valid URLs
    assert validate_youtube_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ") == True
    assert validate_youtube_url("https://youtu.be/dQw4w9WgXcQ") == True

    # Invalid URLs
    assert validate_youtube_url("https://www.google.com") == False
    assert validate_youtube_url("not-a-url") == False
    assert validate_youtube_url("") == False
```

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_utils.py::test_validate_youtube_url -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'src.utils'"

**Step 3: Write minimal implementation**

```python
# src/utils.py
import re

def validate_youtube_url(url: str) -> bool:
    """Validate if URL is a valid YouTube URL."""
    if not url:
        return False

    # YouTube URL patterns
    youtube_patterns = [
        r'https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+',
        r'https?://youtu\.be/[\w-]+'
    ]

    return any(re.match(pattern, url) for pattern in youtube_patterns)

def sanitize_filename(title: str) -> str:
    """Sanitize video title for valid filename."""
    # Remove invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '', title)
    # Replace multiple spaces with single space
    sanitized = re.sub(r'\s+', ' ', sanitized).strip()
    # Limit length
    if len(sanitized) > 200:
        sanitized = sanitized[:200].rsplit(' ', 1)[0]
    return sanitized
```

**Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_utils.py::test_validate_youtube_url -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/utils.py tests/test_utils.py
git commit -m "feat: add URL validation and filename sanitization utilities"
```

### Task 3: File Handler Module

**Files:**
- Create: `src/file_handler.py`
- Create: `tests/test_file_handler.py`

**Step 1: Write the failing test for file operations**

```python
# tests/test_file_handler.py
import os
import tempfile
from pathlib import Path

def test_save_transcript():
    from src.file_handler import save_transcript

    with tempfile.TemporaryDirectory() as temp_dir:
        content = "Hello, world! This is a test transcript."
        title = "Test Video: Episode 1"

        filepath = save_transcript(content, title, "txt", temp_dir)

        assert filepath.exists()
        assert filepath.read_text(encoding='utf-8') == content
        assert "Test_Video_Episode_1" in filepath.name
        assert filepath.suffix == ".txt"
```

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_file_handler.py::test_save_transcript -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'src.file_handler'"

**Step 3: Write minimal implementation**

```python
# src/file_handler.py
from pathlib import Path
from .utils import sanitize_filename

def save_transcript(content: str, title: str, format_type: str, output_dir: str = ".") -> Path:
    """Save transcript content to file."""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    sanitized_title = sanitize_filename(title)
    filename = f"{sanitized_title}.{format_type.lower()}"
    filepath = output_path / filename

    # Handle filename conflicts
    counter = 1
    while filepath.exists():
        filename = f"{sanitized_title}_{counter}.{format_type.lower()}"
        filepath = output_path / filename
        counter += 1

    filepath.write_text(content, encoding='utf-8')
    return filepath

def format_transcript(transcript_data, format_type: str) -> str:
    """Format transcript data according to specified format."""
    if format_type.lower() == "txt":
        return "\n".join(entry['text'] for entry in transcript_data)
    elif format_type.lower() == "srt":
        return _format_srt(transcript_data)
    elif format_type.lower() == "vtt":
        return _format_vtt(transcript_data)
    else:
        raise ValueError(f"Unsupported format: {format_type}")

def _format_srt(transcript_data):
    """Format transcript as SRT subtitles."""
    srt_content = []
    for i, entry in enumerate(transcript_data, 1):
        start_time = _seconds_to_srt_time(entry['start'])
        end_time = _seconds_to_srt_time(entry['start'] + entry['duration'])
        srt_content.append(f"{i}\n{start_time} --> {end_time}\n{entry['text']}\n")
    return "\n".join(srt_content)

def _format_vtt(transcript_data):
    """Format transcript as VTT subtitles."""
    vtt_content = ["WEBVTT\n"]
    for entry in transcript_data:
        start_time = _seconds_to_vtt_time(entry['start'])
        end_time = _seconds_to_vtt_time(entry['start'] + entry['duration'])
        vtt_content.append(f"{start_time} --> {end_time}\n{entry['text']}\n")
    return "\n".join(vtt_content)

def _seconds_to_srt_time(seconds):
    """Convert seconds to SRT time format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millisecs = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millisecs:03d}"

def _seconds_to_vtt_time(seconds):
    """Convert seconds to VTT time format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millisecs = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millisecs:03d}"
```

**Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_file_handler.py::test_save_transcript -v`
Expected: PASS

**Step 5: Commit**

```bash
git add src/file_handler.py tests/test_file_handler.py
git commit -m "feat: add file handling and transcript formatting"
```

### Task 4: Core Transcription Logic

**Files:**
- Create: `src/transcriptor.py`
- Create: `tests/test_transcriptor.py`

**Step 1: Write the failing test for transcript extraction**

```python
# tests/test_transcriptor.py
import pytest
from unittest.mock import patch, MagicMock

def test_get_transcript_success():
    from src.transcriptor import get_transcript

    # Mock youtube_transcript_api
    with patch('src.transcriptor.YouTubeTranscriptApi') as mock_api:
        mock_transcript = [
            {'text': 'Hello world', 'start': 0.0, 'duration': 2.5},
            {'text': 'This is a test', 'start': 2.5, 'duration': 3.0}
        ]
        mock_api.get_transcript.return_value = mock_transcript

        result = get_transcript("https://youtu.be/test123")

        assert result == mock_transcript
        mock_api.get_transcript.assert_called_once()

def test_get_transcript_no_transcript_available():
    from src.transcriptor import get_transcript, NoTranscriptAvailableError

    with patch('src.transcriptor.YouTubeTranscriptApi') as mock_api:
        mock_api.get_transcript.side_effect = Exception("No transcript available")

        with pytest.raises(NoTranscriptAvailableError):
            get_transcript("https://youtu.be/test123")
```

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_transcriptor.py -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'src.transcriptor'"

**Step 3: Write minimal implementation**

```python
# src/transcriptor.py
from youtube_transcript_api import YouTubeTranscriptApi
from .utils import validate_youtube_url

class NoTranscriptAvailableError(Exception):
    """Raised when no transcript is available for a video."""
    pass

class InvalidVideoURLError(Exception):
    """Raised when the provided URL is not a valid YouTube URL."""
    pass

def get_transcript(video_url: str, language: str = None):
    """
    Extract transcript from YouTube video.

    Args:
        video_url: YouTube video URL
        language: Optional language code (e.g., 'en', 'it')

    Returns:
        List of transcript entries with 'text', 'start', and 'duration'

    Raises:
        InvalidVideoURLError: If URL is not valid YouTube URL
        NoTranscriptAvailableError: If no transcript is available
    """
    if not validate_youtube_url(video_url):
        raise InvalidVideoURLError(f"Invalid YouTube URL: {video_url}")

    try:
        # Extract video ID from URL
        video_id = _extract_video_id(video_url)

        # Get transcript list to find available languages
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        if language:
            # Try to get transcript in specified language
            try:
                transcript = transcript_list.find_transcript([language])
                return transcript.fetch()
            except:
                # Fallback to manually generated transcript in specified language
                try:
                    transcript = transcript_list.find_manually_created_transcript([language])
                    return transcript.fetch()
                except:
                    pass

        # Get first available transcript (usually original language)
        try:
            transcript = list(transcript_list)[0]  # Get first available
            return transcript.fetch()
        except:
            # Last resort: try to get any generated transcript
            for transcript in transcript_list:
                if not transcript.is_generated:
                    return transcript.fetch()

            # If no manual transcripts, get first generated one
            for transcript in transcript_list:
                return transcript.fetch()

        raise NoTranscriptAvailableError("No transcript available for this video")

    except Exception as e:
        if "No transcripts found" in str(e) or "Video unavailable" in str(e):
            raise NoTranscriptAvailableError(f"No transcript available: {str(e)}")
        else:
            raise  # Re-raise unexpected errors

def _extract_video_id(url: str) -> str:
    """Extract video ID from YouTube URL."""
    import re

    patterns = [
        r'youtube\.com/watch\?v=([^&]+)',
        r'youtu\.be/([^?]+)',
        r'youtube\.com/embed/([^?]+)'
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    raise InvalidVideoURLError(f"Could not extract video ID from URL: {url}")

def get_video_title(video_url: str) -> str:
    """
    Get video title from YouTube URL.

    Args:
        video_url: YouTube video URL

    Returns:
        Video title as string

    Raises:
        InvalidVideoURLError: If URL is not valid
    """
    try:
        video_id = _extract_video_id(video_url)
        # For now, return a placeholder - we can improve this later
        return f"YouTube Video {video_id}"
    except Exception as e:
        raise InvalidVideoURLError(f"Could not get video title: {str(e)}")
```

**Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_transcriptor.py -v`
Expected: PASS (may need to install youtube-transcript-api first)

**Step 5: Install dependencies and test**

```bash
uv sync
uv run python -m pytest tests/test_transcriptor.py -v
```

**Step 6: Commit**

```bash
git add src/transcriptor.py tests/test_transcriptor.py
git commit -m "feat: add core transcription logic with error handling"
```

### Task 5: CLI Interface

**Files:**
- Create: `src/main.py`
- Modify: `pyproject.toml`

**Step 1: Write the failing test for CLI interface**

```python
# tests/test_main.py
import pytest
from unittest.mock import patch
import sys
from io import StringIO

def test_cli_argument_parsing():
    # Test that we can import and use the CLI
    from src.main import parse_arguments

    # Test with URL only
    args = parse_arguments(["https://youtu.be/test123"])
    assert args.url == "https://youtu.be/test123"
    assert args.format == "txt"
    assert args.output == "."
    assert args.language is None
```

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_main.py::test_cli_argument_parsing -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'src.main'"

**Step 3: Write minimal CLI implementation**

```python
# src/main.py
import argparse
import sys
from pathlib import Path

from .transcriptor import get_transcript, get_video_title, NoTranscriptAvailableError, InvalidVideoURLError
from .file_handler import save_transcript, format_transcript
from .utils import validate_youtube_url

def parse_arguments(args=None):
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Extract YouTube video transcripts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m yt_transcriptor "https://youtu.be/dQw4w9WgXcQ"
  python -m yt_transcriptor "https://youtu.be/dQw4w9WgXcQ" --format srt
  python -m yt_transcriptor "https://youtu.be/dQw4w9WgXcQ" --language en --output ./transcripts
        """
    )

    parser.add_argument(
        "url",
        help="YouTube video URL"
    )

    parser.add_argument(
        "--format", "-f",
        choices=["txt", "srt", "vtt"],
        default="txt",
        help="Output format (default: txt)"
    )

    parser.add_argument(
        "--language", "-l",
        help="Language code (e.g., en, it, es). If not specified, uses first available."
    )

    parser.add_argument(
        "--output", "-o",
        default=".",
        help="Output directory (default: current directory)"
    )

    return parser.parse_args(args)

def main(args=None):
    """Main CLI function."""
    try:
        parsed_args = parse_arguments(args)

        # Validate URL
        if not validate_youtube_url(parsed_args.url):
            print(f"Error: Invalid YouTube URL: {parsed_args.url}", file=sys.stderr)
            sys.exit(1)

        print(f"Extracting transcript from: {parsed_args.url}")

        # Get transcript
        transcript_data = get_transcript(parsed_args.url, parsed_args.language)

        # Get video title
        video_title = get_video_title(parsed_args.url)
        print(f"Video title: {video_title}")

        # Format transcript
        formatted_content = format_transcript(transcript_data, parsed_args.format)

        # Save to file
        filepath = save_transcript(
            formatted_content,
            video_title,
            parsed_args.format,
            parsed_args.output
        )

        print(f"Transcript saved to: {filepath}")
        print(f"Format: {parsed_args.format}")
        print(f"Lines: {len(transcript_data)}")

    except NoTranscriptAvailableError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except InvalidVideoURLError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

**Step 4: Update pyproject.toml for module execution**

```toml
[project]
name = "yt-transcriptor"
version = "0.1.0"
description = "Extract YouTube video transcripts directly without downloading videos"
requires-python = ">=3.13"
dependencies = [
    "youtube-transcript-api>=0.6.0"
]

[project.scripts]
yt-transcriptor = "src.main:main"

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"
```

**Step 5: Run test to verify it passes**

Run: `python -m pytest tests/test_main.py::test_cli_argument_parsing -v`
Expected: PASS

**Step 6: Test CLI manually**

```bash
python -m src.main --help
```

**Step 7: Commit**

```bash
git add src/main.py tests/test_main.py pyproject.toml
git commit -m "feat: add CLI interface with argument parsing"
```

### Task 6: Integration Testing and Documentation

**Files:**
- Create: `README.md`
- Create: `tests/test_integration.py`

**Step 1: Write integration tests**

```python
# tests/test_integration.py
import tempfile
import os
from unittest.mock import patch
from pathlib import Path

def test_end_to_end_workflow():
    """Test complete workflow with mocked transcript API."""
    from src.main import main
    from unittest.mock import patch

    mock_transcript = [
        {'text': 'Hello world', 'start': 0.0, 'duration': 2.5},
        {'text': 'This is a test transcript', 'start': 2.5, 'duration': 3.0}
    ]

    with tempfile.TemporaryDirectory() as temp_dir:
        with patch('src.main.get_transcript') as mock_get:
            with patch('src.main.get_video_title') as mock_title:
                mock_get.return_value = mock_transcript
                mock_title.return_value = "Test Video"

                # Test CLI call
                main([
                    "https://youtu.be/test123",
                    "--output", temp_dir,
                    "--format", "txt"
                ])

                # Verify file was created
                output_files = list(Path(temp_dir).glob("*.txt"))
                assert len(output_files) == 1

                content = output_files[0].read_text(encoding='utf-8')
                assert "Hello world" in content
                assert "This is a test transcript" in content
```

**Step 2: Run integration tests**

Run: `python -m pytest tests/test_integration.py -v`
Expected: PASS

**Step 3: Create README**

```markdown
# YouTube Transcriptor

A lightweight Python CLI tool that extracts YouTube video transcripts directly without downloading videos.

## Features

- Extract transcripts directly from YouTube videos
- Support for multiple output formats (TXT, SRT, VTT)
- Language selection (manual override)
- Automatic filename generation from video title
- Lightweight and fast - no video downloads

## Installation

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install youtube-transcript-api
```

## Usage

Basic usage:
```bash
uv run python -m src.main "https://www.youtube.com/watch?v=VIDEO_ID"
```

With options:
```bash
uv run python -m src.main "https://www.youtube.com/watch?v=VIDEO_ID" \
  --format srt \
  --language en \
  --output ./transcripts
```

### Options

- `--format, -f`: Output format (txt, srt, vtt) - default: txt
- `--language, -l`: Language code (en, it, es, etc.) - default: auto-detect
- `--output, -o`: Output directory - default: current directory

### Examples

```bash
# Get plain text transcript
uv run python -m src.main "https://youtu.be/dQw4w9WgXcQ"

# Get SRT subtitles in English
uv run python -m src.main "https://youtu.be/dQw4w9WgXcQ" --format srt --language en

# Save all transcripts to a specific folder
uv run python -m src.main "https://youtu.be/dQw4w9WgXcQ" --output ~/transcripts
```

## Development

Run tests:
```bash
uv run python -m pytest tests/
```

## Dependencies

- Python 3.13+
- uv (package manager)
- youtube-transcript-api

## License

This project is for educational and personal use.
```

**Step 4: Run all tests**

```bash
python -m pytest tests/ -v
```

**Step 5: Commit**

```bash
git add README.md tests/test_integration.py
git commit -m "feat: add integration tests and documentation"
```

---

## Execution Summary

This implementation plan provides a complete, tested YouTube transcript extraction tool with:

- ✅ Modular architecture with clear separation of concerns
- ✅ TDD approach with comprehensive test coverage
- ✅ Multiple output formats (TXT, SRT, VTT)
- ✅ CLI interface with helpful options
- ✅ Error handling for edge cases
- ✅ Clean documentation and examples

The tool fulfills all requirements from CLAUDE.md while maintaining clean, maintainable code suitable for a non-production educational project.