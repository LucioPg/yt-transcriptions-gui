# tests/test_file_handler.py
import os
import tempfile
from pathlib import Path

def test_save_transcript():
    from src.file_handler import save_transcript

    with tempfile.TemporaryDirectory() as temp_dir:
        content = "Hello, world! This is a test transcript."
        title = "Test Video: Episode 1"

        filepath = save_transcript(content, title, "txt", temp_dir)

        assert filepath.exists()
        assert filepath.read_text(encoding='utf-8') == content
        assert "Test_Video_Episode_1" in filepath.name
        assert filepath.suffix == ".txt"

def test_format_transcript_txt():
    from src.file_handler import format_transcript

    transcript_data = [
        {'text': 'Hello world', 'start': 0.0, 'duration': 2.5},
        {'text': 'This is a test', 'start': 2.5, 'duration': 3.0}
    ]

    result = format_transcript(transcript_data, "txt")
    expected = "Hello world\nThis is a test"
    assert result == expected

def test_format_transcript_srt():
    from src.file_handler import format_transcript

    transcript_data = [
        {'text': 'Hello world', 'start': 0.0, 'duration': 2.5},
        {'text': 'This is a test', 'start': 2.5, 'duration': 3.0}
    ]

    result = format_transcript(transcript_data, "srt")
    lines = result.strip().split('\n')

    # Should have sequence numbers, timestamps, and text
    assert "1" in lines
    assert "00:00:00,000 --> 00:00:02,500" in lines
    assert "Hello world" in lines
    assert "2" in lines
    assert "00:00:02,500 --> 00:00:05,500" in lines
    assert "This is a test" in lines

def test_format_transcript_vtt():
    from src.file_handler import format_transcript

    transcript_data = [
        {'text': 'Hello world', 'start': 0.0, 'duration': 2.5}
    ]

    result = format_transcript(transcript_data, "vtt")
    assert result.startswith("WEBVTT")
    assert "00:00:00.000 --> 00:00:02.500" in result
    assert "Hello world" in result