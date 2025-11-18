# tests/test_transcriptor.py
import pytest
from unittest.mock import patch, MagicMock

def test_get_transcript_success():
    from src.transcriptor import get_transcript

    # Mock youtube_transcript_api
    with patch('src.transcriptor.YouTubeTranscriptApi') as mock_api:
        mock_transcript = [
            {'text': 'Hello world', 'start': 0.0, 'duration': 2.5},
            {'text': 'This is a test', 'start': 2.5, 'duration': 3.0}
        ]

        # Mock transcript object
        mock_transcript_obj = MagicMock()
        mock_transcript_obj.fetch.return_value = mock_transcript

        # Mock transcript list
        mock_transcript_list = MagicMock()
        mock_transcript_list.__iter__.return_value = [mock_transcript_obj]

        mock_api.list_transcripts.return_value = mock_transcript_list

        result = get_transcript("https://youtu.be/test123")

        assert result == mock_transcript
        mock_api.list_transcripts.assert_called_once_with("test123")

def test_get_transcript_no_transcript_available():
    from src.transcriptor import get_transcript, NoTranscriptAvailableError

    with patch('src.transcriptor.YouTubeTranscriptApi') as mock_api:
        mock_api.list_transcripts.side_effect = Exception("No transcripts found")

        with pytest.raises(NoTranscriptAvailableError):
            get_transcript("https://youtu.be/test123")

def test_extract_video_id():
    from src.transcriptor import _extract_video_id

    # Test different YouTube URL formats
    assert _extract_video_id("https://www.youtube.com/watch?v=abc123") == "abc123"
    assert _extract_video_id("https://youtu.be/def456") == "def456"
    assert _extract_video_id("https://youtube.com/embed/ghi789") == "ghi789"

def test_invalid_url_raises_error():
    from src.transcriptor import get_transcript, InvalidVideoURLError

    with pytest.raises(InvalidVideoURLError):
        get_transcript("https://www.google.com")

def test_get_video_title():
    from src.transcriptor import get_video_title

    title = get_video_title("https://youtu.be/test123")
    assert title == "YouTube Video test123"