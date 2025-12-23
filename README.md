# YouTube Transcriptions GUI

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A Python tool that extracts YouTube video transcripts directly without downloading videos. Features both CLI and web interfaces.

## Features

- **Direct Transcript Extraction**: Download transcripts without video downloads
- **Dual Interface**: Both CLI and web interface
- **Multiple Output Formats**: Support for TXT, SRT, and VTT formats
- **Language Selection**: Manual language override or auto-detection
- **File Management**: Automatic filename generation based on video title
- **Web Interface**: Simple interface using FastAPI and Jinja2 templates
- **Error Handling**: Comprehensive error handling with clear messages

## Requirements

- Python 3.13+
- uv package manager (recommended)

## Installation

```bash
# Clone the repository
git clone https://github.com/LucioPG/yt-transcriptions-gui.git
cd yt-transcriptions-gui

# Install dependencies
uv sync
```

## Usage

### CLI Interface

```bash
# Basic usage
uv run python -m src.cli_main "https://www.youtube.com/watch?v=VIDEO_ID"

# Advanced usage
uv run python -m src.cli_main "https://www.youtube.com/watch?v=VIDEO_ID" \
  --format srt \
  --language en \
  --output ./transcripts

# Help
uv run python -m src.cli_main --help
```

### Web Interface

```bash
# Start the web server
uv run python -m src.web_main

# The application will:
# - Start the server on http://localhost:8031
# - Open the browser automatically
# - Save transcripts to ~/yt-transcriptions/
```

## Command Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--format` | `-f` | Output format (txt, srt, vtt) | `txt` |
| `--language` | `-l` | Language code (en, it, es, etc.) | auto-detect |
| `--output` | `-o` | Output directory | `transcriptions` |

## Output Formats

### TXT Format
Plain text transcript suitable for reading and documentation.

```
Hello world, this is a transcript example.
This is the second line of the transcript.
```

### SRT Format
Standard subtitle format compatible with video players.

```srt
1
00:00:00,000 --> 00:00:02,500
Hello world, this is a transcript example.

2
00:00:02,500 --> 00:00:05,000
This is the second line of the transcript.
```

### VTT Format
Web Video Text Tracks format for web applications.

```vtt
WEBVTT

00:00:00.000 --> 00:00:02.500
Hello world, this is a transcript example.

00:00:02.500 --> 00:00:05.000
This is the second line of the transcript.
```

## Architecture

```
YouTube Transcriptions GUI
├── CLI Interface (cli_main.py)
│   └── Command-line interface for advanced users
├── Web Interface (web_main.py)
│   └── Web interface with FastAPI
└── Core Logic
    ├── transcriptor.py: YouTube API integration
    ├── file_handler.py: File operations
    └── utils.py: Utilities and validation
```

## Testing

```bash
# Run all tests
uv run python -m pytest tests/

# Run with coverage report
uv run python -m pytest tests/ --cov=src --cov-report=html

# Run specific test file
uv run python -m pytest tests/test_transcriptor.py
```

## Building Windows Executables

```bash
# Install packaging dependencies
uv sync --extra packaging

# Build CLI executable
uv run pyinstaller --onefile --console --name "yt-transcriptions-gui-cli" src/cli_main.py

# Build Web executable
uv run pyinstaller --onefile --windowed \
  --add-data "src/templates;templates" \
  --add-data "src/static;static" \
  --name "yt-transcriptions-gui-web" \
  src/web_main.py
```

## Project Structure

```
yt-transcriptions-gui/
├── src/                     # Source code
│   ├── cli_main.py         # CLI entry point
│   ├── web_main.py         # Web entry point
│   ├── transcriptor.py     # Core transcript extraction
│   ├── file_handler.py     # File operations and formatting
│   ├── utils.py            # Utility functions
│   ├── templates/          # HTML templates
│   └── static/             # Static files (CSS, JS)
├── tests/                  # Test suite
├── dist/                   # Built executables
└── transcriptions/         # Default CLI output directory
```

## Dependencies

### Runtime Dependencies
- **Python 3.13+**: Modern Python
- **fastapi**: Web framework
- **uvicorn**: ASGI server
- **jinja2**: Template engine
- **youtube-transcript-api**: YouTube transcript extraction

### Development Dependencies
- **pytest**: Testing framework
- **coverage**: Code coverage measurement

## Supported URL Formats

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`

## Error Handling

The tool provides error handling for common issues:

- **Invalid URLs**: Clear validation and error messages
- **Missing Transcripts**: Graceful handling when no transcript is available
- **Network Issues**: Timeout and connection error handling
- **Language Issues**: Fallback handling for unavailable languages

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) for the core transcript extraction functionality

---

Note: This tool is for educational and personal use. Please respect YouTube's Terms of Service and copyright laws when using extracted transcripts.
