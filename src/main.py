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
        default="transcriptions",
        help="Output directory (default: transcriptions)"
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