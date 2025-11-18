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