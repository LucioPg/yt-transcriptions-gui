# tests/test_integration.py
import tempfile
import os
from unittest.mock import patch
from pathlib import Path
import shutil

def test_end_to_end_workflow():
    """Test complete workflow with mocked transcript API."""
    from src.main import main
    from unittest.mock import patch

    # Mock transcript objects as returned by YouTubeTranscriptApi.fetch()
    from unittest.mock import Mock

    mock_snippet1 = Mock()
    mock_snippet1.text = 'Hello world'
    mock_snippet1.start = 0.0
    mock_snippet1.duration = 2.5

    mock_snippet2 = Mock()
    mock_snippet2.text = 'This is a test transcript'
    mock_snippet2.start = 2.5
    mock_snippet2.duration = 3.0

    mock_transcript = [mock_snippet1, mock_snippet2]

    with tempfile.TemporaryDirectory() as temp_dir:
        with patch('src.main.get_transcript') as mock_get:
            with patch('src.main.get_video_title') as mock_title:
                mock_get.return_value = mock_transcript
                mock_title.return_value = "Test Video"

                # Test CLI call
                main([
                    "https://youtu.be/test123",
                    "--output", temp_dir,
                    "--format", "txt"
                ])

                # Verify file was created
                output_files = list(Path(temp_dir).glob("*.txt"))
                assert len(output_files) == 1

                content = output_files[0].read_text(encoding='utf-8')
                assert "Hello world" in content
                assert "This is a test transcript" in content

def test_default_output_directory():
    """Test that transcriptions directory is created and used by default."""
    from src.main import main
    from unittest.mock import Mock

    # Clean up any existing transcriptions directory
    transcriptions_dir = Path("transcriptions")
    if transcriptions_dir.exists():
        shutil.rmtree(transcriptions_dir)

    # Mock transcript objects
    mock_snippet = Mock()
    mock_snippet.text = 'Test content for default directory'
    mock_snippet.start = 0.0
    mock_snippet.duration = 2.0

    mock_transcript = [mock_snippet]

    try:
        with patch('src.main.get_transcript') as mock_get:
            with patch('src.main.get_video_title') as mock_title:
                mock_get.return_value = mock_transcript
                mock_title.return_value = "Test Video Default"

                # Test CLI call without --output argument (uses default)
                main([
                    "https://youtu.be/test123",
                    "--format", "txt"
                ])

                # Verify transcriptions directory was created
                assert transcriptions_dir.exists()
                assert transcriptions_dir.is_dir()

                # Verify file was created in transcriptions directory
                output_files = list(transcriptions_dir.glob("*.txt"))
                assert len(output_files) == 1

                content = output_files[0].read_text(encoding='utf-8')
                assert "Test content for default directory" in content

    finally:
        # Clean up the transcriptions directory
        if transcriptions_dir.exists():
            shutil.rmtree(transcriptions_dir)