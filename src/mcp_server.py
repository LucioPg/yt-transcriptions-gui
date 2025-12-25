# src/mcp_server.py
"""
MCP Server for YouTube Transcriptor

Exposes transcript extraction tools via the Model Context Protocol (MCP).
Uses stdio transport for communication with MCP clients.
"""

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import Literal, Optional

# Handle both relative and absolute imports for different execution contexts
try:
    from .transcriptor import get_transcript as fetch_transcript, get_video_title, NoTranscriptAvailableError, InvalidVideoURLError
    from .file_handler import format_transcript
except ImportError:
    from transcriptor import get_transcript as fetch_transcript, get_video_title, NoTranscriptAvailableError, InvalidVideoURLError
    from file_handler import format_transcript


class TranscriptResult(BaseModel):
    """Structured result for transcript extraction."""
    video_url: str = Field(description="Original YouTube video URL")
    video_title: str = Field(description="Title of the video")
    content: str = Field(description="Full transcript text in requested format")
    language: Optional[str] = Field(default=None, description="Language code of transcript")
    format: Literal["txt", "vtt", "srt"] = Field(description="Output format")
    segments_count: int = Field(description="Number of transcript segments")


# Initialize MCP server with stdio transport (default)
mcp = FastMCP(
    "YouTube Transcriptor",
    instructions=(
        "Extract transcripts from YouTube videos without downloading. "
        "Supports txt, vtt (with timestamps for citations), and srt formats. "
        "Auto-detects language (en, it) or accepts specific language codes."
    )
)


@mcp.tool()
def get_transcript(
    url: str,
    format: Literal["txt", "vtt", "srt"] = "txt",
    language: Optional[str] = None
) -> TranscriptResult:
    """
    Extract transcript from YouTube video.

    Args:
        url: YouTube video URL
        format: Output format - txt (default), vtt (with timestamps for citations), or srt
        language: Optional language code (e.g., 'en', 'it'). Auto-detects if not specified.

    Returns:
        TranscriptResult JSON with video_url, video_title, content, language, format, segments_count

    Raises:
        InvalidVideoURLError: If URL is not valid YouTube URL
        NoTranscriptAvailableError: If no transcript is available for video
    """
    # Get transcript data
    transcript_data = fetch_transcript(url, language)
    video_title = get_video_title(url)
    formatted_content = format_transcript(transcript_data, format)

    return TranscriptResult(
        video_url=url,
        video_title=video_title,
        content=formatted_content,
        language=language,
        format=format,
        segments_count=len(transcript_data)
    )


def main():
    """Entry point for MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
