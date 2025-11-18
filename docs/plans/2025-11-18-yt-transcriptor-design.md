# YouTube Transcriptor CLI Tool - Design Document

## Overview
A lightweight Python CLI tool that extracts YouTube video transcripts directly without downloading videos, maintaining original language and supporting multiple output formats.

## Architecture

### Core Components
- **main.py**: CLI entry point with argument parsing and user interface
- **transcriptor.py**: Core logic for extracting transcripts using youtube-transcript-api
- **file_handler.py**: File saving operations and name sanitization
- **utils.py**: Utility functions for validation and formatting

### Data Flow
1. CLI receives YouTube URL as argument
2. URL validation and video metadata extraction
3. Transcript extraction using youtube-transcript-api
4. Language handling (default: first available transcript, manual override optional)
5. Title sanitization for valid filename
6. Save transcript in specified format

## Technical Specifications

### Dependencies
- `youtube-transcript-api` (primary transcript extraction)
- `argparse` (CLI interface - built-in)
- `pathlib` (file operations - built-in)
- `re` (text sanitization - built-in)

### CLI Interface
```bash
python -m yt_transcriptor <URL> [options]
--format txt|srt|vtt    # Output format (default: txt)
--language <code>        # Override language (en, it, es, etc.)
--output <dir>          # Output directory (default: current directory)
```

### Language Handling Strategy
- **Default**: Use first available transcript (typically original language)
- **Manual override**: `--language` parameter for explicit selection
- **Fallback**: Graceful handling when no transcripts available

### Error Handling
- Invalid URLs or non-existent videos
- Videos without available transcripts
- Network connectivity issues
- File system permission problems
- Invalid language codes

### Output Formats
- **TXT** (default): Plain text transcript
- **SRT**: Subtitle format with timestamps
- **VTT**: Web Video Text Tracks format

### File Naming
- Filename based on video title
- Sanitization of special characters for valid filenames
- Conflict resolution (append counter if filename exists)

## Project Structure
```
yt-transcriptor/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── transcriptor.py
│   ├── file_handler.py
│   └── utils.py
├── docs/
│   └── plans/
│       └── 2025-11-18-yt-transcriptor-design.md
├── requirements.txt
├── README.md
├── CLAUDE.md
└── pyproject.toml
```

## Implementation Notes
- Non-production grade: focus on functionality over robustness
- CLI-first approach with future web interface possibility
- Python 3.13+ compatibility
- Simple, readable code structure
- Italian project with English technical documentation