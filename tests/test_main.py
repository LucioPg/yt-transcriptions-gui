# tests/test_main.py
import pytest
from unittest.mock import patch, Mock
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

    # Mock transcript objects as returned by YouTubeTranscriptApi.fetch()
    mock_snippet1 = Mock()
    mock_snippet1.text = "Hello world"
    mock_snippet1.start = 0.0
    mock_snippet1.duration = 2.5

    mock_snippet2 = Mock()
    mock_snippet2.text = "This is a test"
    mock_snippet2.start = 2.5
    mock_snippet2.duration = 3.0

    mock_transcript = [mock_snippet1, mock_snippet2]

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

def test_main_function_invalid_url():
    """Test main function with invalid URL."""
    from src.main import main

    # Capture stderr
    captured_error = StringIO()

    with patch('sys.stderr', captured_error):
        with pytest.raises(SystemExit) as exc_info:
            main(["https://www.google.com"])

    assert exc_info.value.code == 1
    error_output = captured_error.getvalue()
    assert "Error: Invalid YouTube URL:" in error_output
    assert "https://www.google.com" in error_output

def test_main_function_no_transcript_available():
    """Test main function when no transcript is available."""
    from src.main import main
    from src.transcriptor import NoTranscriptAvailableError

    # Mock get_transcript to raise NoTranscriptAvailableError
    with patch('src.main.get_transcript') as mock_get:
        mock_get.side_effect = NoTranscriptAvailableError("No transcript found")

        # Capture stderr
        captured_error = StringIO()

        with patch('sys.stderr', captured_error):
            with pytest.raises(SystemExit) as exc_info:
                main(["https://youtu.be/test123"])

        assert exc_info.value.code == 1
        error_output = captured_error.getvalue()
        assert "Error: No transcript found" in error_output

def test_main_function_invalid_video_url():
    """Test main function when video URL is invalid."""
    from src.main import main
    from src.transcriptor import InvalidVideoURLError

    # Mock get_transcript to raise InvalidVideoURLError
    with patch('src.main.get_transcript') as mock_get:
        mock_get.side_effect = InvalidVideoURLError("Invalid video URL")

        # Capture stderr
        captured_error = StringIO()

        with patch('sys.stderr', captured_error):
            with pytest.raises(SystemExit) as exc_info:
                main(["https://youtu.be/test123"])

        assert exc_info.value.code == 1
        error_output = captured_error.getvalue()
        assert "Error: Invalid video URL" in error_output

def test_main_function_unexpected_error():
    """Test main function with unexpected error."""
    from src.main import main

    # Mock get_transcript to raise unexpected error
    with patch('src.main.get_transcript') as mock_get:
        mock_get.side_effect = ValueError("Database connection failed")

        # Capture stderr
        captured_error = StringIO()

        with patch('sys.stderr', captured_error):
            with pytest.raises(SystemExit) as exc_info:
                main(["https://youtu.be/test123"])

        assert exc_info.value.code == 1
        error_output = captured_error.getvalue()
        assert "Unexpected error: Database connection failed" in error_output