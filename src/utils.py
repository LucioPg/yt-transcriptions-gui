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
    # Replace spaces with underscores for filenames
    sanitized = re.sub(r'\s+', '_', sanitized.strip())
    # Remove multiple underscores
    sanitized = re.sub(r'_+', '_', sanitized)
    # Limit length
    if len(sanitized) > 200:
        sanitized = sanitized[:200].rsplit('_', 1)[0]
    return sanitized