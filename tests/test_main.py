# tests/test_main.py
import pytest
from unittest.mock import patch
import sys
from io import StringIO

def test_cli_argument_parsing():
    # Test that we can import and use the CLI
    from src.main import parse_arguments

    # Test with URL only
    args = parse_arguments(["https://youtu.be/test123"])
    assert args.url == "https://youtu.be/test123"
    assert args.format == "txt"
    assert args.output == "."
    assert args.language is None

def test_cli_argument_parsing_with_options():
    from src.main import parse_arguments

    # Test with all options
    args = parse_arguments([
        "https://youtu.be/test123",
        "--format", "srt",
        "--language", "en",
        "--output", "./transcripts"
    ])

    assert args.url == "https://youtu.be/test123"
    assert args.format == "srt"
    assert args.language == "en"
    assert args.output == "./transcripts"

def test_main_function_success():
    from src.main import main

    mock_transcript = [
        {'text': 'Hello world', 'start': 0.0, 'duration': 2.5},
        {'text': 'This is a test', 'start': 2.5, 'duration': 3.0}
    ]

    with patch('src.main.get_transcript') as mock_get:
        with patch('src.main.get_video_title') as mock_title:
            with patch('src.main.save_transcript') as mock_save:
                mock_get.return_value = mock_transcript
                mock_title.return_value = "Test Video"
                mock_save.return_value = "/tmp/test_transcript.txt"

                # Capture stdout
                captured_output = StringIO()

                with patch('sys.stdout', captured_output):
                    main([
                        "https://youtu.be/test123",
                        "--format", "txt"
                    ])

                output = captured_output.getvalue()
                assert "Extracting transcript from:" in output
                assert "Video title: Test Video" in output
                assert "Transcript saved to:" in output
                assert "Format: txt" in output
                assert "Lines: 2" in output