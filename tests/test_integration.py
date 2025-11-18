# tests/test_integration.py
import tempfile
import os
from unittest.mock import patch
from pathlib import Path

def test_end_to_end_workflow():
    """Test complete workflow with mocked transcript API."""
    from src.main import main
    from unittest.mock import patch

    mock_transcript = [
        {'text': 'Hello world', 'start': 0.0, 'duration': 2.5},
        {'text': 'This is a test transcript', 'start': 2.5, 'duration': 3.0}
    ]

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