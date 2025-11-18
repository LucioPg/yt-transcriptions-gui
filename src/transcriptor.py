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

        # Try to get transcript with language preference
        api = YouTubeTranscriptApi()

        if language:
            # Try to get transcript in specified language
            try:
                return api.fetch(video_id, languages=[language])
            except:
                pass

        # Get transcript in default language (English)
        try:
            return api.fetch(video_id)
        except Exception as e:
            if "No transcripts found" in str(e) or "Video unavailable" in str(e):
                raise NoTranscriptAvailableError(f"No transcript available: {str(e)}")
            else:
                raise  # Re-raise unexpected errors

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