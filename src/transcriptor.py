# src/transcriptor.py
from youtube_transcript_api import YouTubeTranscriptApi

try:
    # Try relative imports first (when run as module)
    from .utils import validate_youtube_url
except ImportError:
    # Fall back to absolute imports (when run as script)
    from utils import validate_youtube_url

class NoTranscriptAvailableError(Exception):
    """Raised when no transcript is available for a video."""
    pass

class InvalidVideoURLError(Exception):
    """Raised when the provided URL is not a valid YouTube URL."""
    pass

def get_transcript(video_url: str, language: str = None):
    """
    Extract transcript from YouTube video with simple language fallback.

    Language resolution:
    1. Try specified language (if provided)
    2. Try 'en' (English)
    3. Try 'it' (Italian) as fallback
    4. Raise "Can not fetch" error if all attempts fail

    Args:
        video_url: YouTube video URL
        language: Optional language code (e.g., 'en', 'it')

    Returns:
        List of transcript entries with 'text', 'start', and 'duration'

    Raises:
        InvalidVideoURLError: If URL is not valid YouTube URL
        NoTranscriptAvailableError: If no transcript can be fetched
    """
    if not validate_youtube_url(video_url):
        raise InvalidVideoURLError(f"Invalid YouTube URL: {video_url}")

    video_id = _extract_video_id(video_url)
    api = YouTubeTranscriptApi()

    # Determine languages to try in order
    languages_to_try = []
    if language:
        languages_to_try.append(language)
    languages_to_try.extend(['en', 'it'])

    # Try each language in sequence
    for lang in languages_to_try:
        try:
            return api.fetch(video_id, languages=[lang])
        except Exception:
            # Try next language
            continue

    # All attempts failed
    raise NoTranscriptAvailableError("Can not fetch transcript")

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