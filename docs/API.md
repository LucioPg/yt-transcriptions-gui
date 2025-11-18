# API Documentation

This document provides detailed API documentation for the YouTube Transcriptor library.

## Table of Contents

- [Core Modules](#core-modules)
  - [transcriptor](#transcriptor)
  - [file_handler](#file_handler)
  - [utils](#utils)
  - [main](#main)
- [Exceptions](#exceptions)
- [Data Structures](#data-structures)

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