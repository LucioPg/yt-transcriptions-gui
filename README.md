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