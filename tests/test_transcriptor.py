# tests/test_transcriptor.py
import pytest
from unittest.mock import Mock, patch, MagicMock, create_autospec

def test_get_transcript_success():
    """Test successful transcript retrieval using proper mocking with autospec."""
    from src.transcriptor import get_transcript
    from youtube_transcript_api import YouTubeTranscriptApi

    # Mock transcript objects as returned by YouTubeTranscriptApi.fetch()
    mock_snippet1 = Mock()
    mock_snippet1.text = "Hello world"
    mock_snippet1.start = 0.0
    mock_snippet1.duration = 2.5

    mock_snippet2 = Mock()
    mock_snippet2.text = "This is a test"
    mock_snippet2.start = 2.5
    mock_snippet2.duration = 3.0

    mock_transcript_data = [mock_snippet1, mock_snippet2]

    # Use create_autospec to ensure we're mocking the real API correctly
    with patch('src.transcriptor.YouTubeTranscriptApi') as mock_api_class:
        # Create autospec of the actual class
        mock_api_instance = create_autospec(YouTubeTranscriptApi)
        mock_api_instance.fetch.return_value = mock_transcript_data
        mock_api_class.return_value = mock_api_instance

        result = get_transcript("https://youtu.be/test123")

        assert result == mock_transcript_data
        assert len(result) == 2
        assert result[0].text == 'Hello world'
        assert result[1].text == 'This is a test'

        # Verify the API was called correctly
        mock_api_instance.fetch.assert_called_once_with("test123")

def test_get_transcript_no_transcript_available():
    """Test NoTranscriptAvailableError when API reports no transcripts."""
    from src.transcriptor import get_transcript, NoTranscriptAvailableError
    from youtube_transcript_api import YouTubeTranscriptApi

    with patch('src.transcriptor.YouTubeTranscriptApi') as mock_api_class:
        mock_api_instance = create_autospec(YouTubeTranscriptApi)
        mock_api_instance.fetch.side_effect = Exception("No transcripts found")
        mock_api_class.return_value = mock_api_instance

        with pytest.raises(NoTranscriptAvailableError, match="No transcript available"):
            get_transcript("https://youtu.be/test123")

def test_get_transcript_with_language():
    """Test transcript retrieval with specific language."""
    from src.transcriptor import get_transcript
    from youtube_transcript_api import YouTubeTranscriptApi

    # Mock transcript object for specific language
    mock_snippet = Mock()
    mock_snippet.text = "English transcript"
    mock_snippet.start = 0.0
    mock_snippet.duration = 2.0

    mock_transcript_data = [mock_snippet]

    with patch('src.transcriptor.YouTubeTranscriptApi') as mock_api_class:
        mock_api_instance = create_autospec(YouTubeTranscriptApi)
        mock_api_instance.fetch.return_value = mock_transcript_data
        mock_api_class.return_value = mock_api_instance

        result = get_transcript("https://youtu.be/test123", language="en")

        assert result == mock_transcript_data
        assert result[0].text == "English transcript"
        mock_api_instance.fetch.assert_called_once_with("test123", languages=['en'])

def test_get_transcript_language_fallback():
    """Test language fallback to default when specified language fails."""
    from src.transcriptor import get_transcript
    from youtube_transcript_api import YouTubeTranscriptApi

    # Mock transcript object for fallback
    mock_snippet = Mock()
    mock_snippet.text = "Default transcript"
    mock_snippet.start = 0.0
    mock_snippet.duration = 2.0

    mock_transcript_data = [mock_snippet]

    with patch('src.transcriptor.YouTubeTranscriptApi') as mock_api_class:
        mock_api_instance = create_autospec(YouTubeTranscriptApi)
        # First call (with language) fails, second call (default) succeeds
        mock_api_instance.fetch.side_effect = [Exception("Language not found"), mock_transcript_data]
        mock_api_class.return_value = mock_api_instance

        result = get_transcript("https://youtu.be/test123", language="nonexistent")

        assert result == mock_transcript_data
        assert result[0].text == "Default transcript"
        # Verify both calls were made
        assert mock_api_instance.fetch.call_count == 2

def test_extract_video_id():
    """Test video ID extraction from various YouTube URL formats."""
    from src.transcriptor import _extract_video_id, InvalidVideoURLError

    # Test different YouTube URL formats
    assert _extract_video_id("https://www.youtube.com/watch?v=abc123") == "abc123"
    assert _extract_video_id("https://youtu.be/def456") == "def456"
    assert _extract_video_id("https://youtube.com/embed/ghi789") == "ghi789"

    # Test URL with additional parameters
    assert _extract_video_id("https://www.youtube.com/watch?v=abc123&t=30s") == "abc123"
    assert _extract_video_id("https://youtu.be/def456?list=PL123") == "def456"

    # Test invalid URL raises error
    with pytest.raises(InvalidVideoURLError):
        _extract_video_id("https://www.google.com")

def test_invalid_url_raises_error():
    """Test that InvalidVideoURLError is raised for invalid YouTube URLs."""
    from src.transcriptor import get_transcript, InvalidVideoURLError

    with pytest.raises(InvalidVideoURLError, match="Invalid YouTube URL"):
        get_transcript("https://www.google.com")

def test_get_video_title():
    """Test video title retrieval."""
    from src.transcriptor import get_video_title, InvalidVideoURLError

    title = get_video_title("https://youtu.be/test123")
    assert title == "YouTube Video test123"

def test_get_video_title_invalid_url():
    """Test that InvalidVideoURLError is raised for invalid URLs when getting title."""
    from src.transcriptor import get_video_title, InvalidVideoURLError

    with patch('src.transcriptor._extract_video_id') as mock_extract:
        mock_extract.side_effect = InvalidVideoURLError("Invalid URL")

        with pytest.raises(InvalidVideoURLError):
            get_video_title("invalid_url")

def test_get_transcript_unexpected_error():
    """Test that unexpected errors are re-raised without catching."""
    from src.transcriptor import get_transcript

    from youtube_transcript_api import YouTubeTranscriptApi

    with patch('src.transcriptor.YouTubeTranscriptApi') as mock_api_class:
        mock_api_instance = create_autospec(YouTubeTranscriptApi)
        mock_api_instance.fetch.side_effect = ValueError("Unexpected database error")
        mock_api_class.return_value = mock_api_instance

        with pytest.raises(ValueError, match="Unexpected database error"):
            get_transcript("https://youtu.be/test123")

def test_get_transcript_video_unavailable():
    """Test NoTranscriptAvailableError when video is unavailable."""
    from src.transcriptor import get_transcript, NoTranscriptAvailableError
    from youtube_transcript_api import YouTubeTranscriptApi

    with patch('src.transcriptor.YouTubeTranscriptApi') as mock_api_class:
        mock_api_instance = create_autospec(YouTubeTranscriptApi)
        mock_api_instance.fetch.side_effect = Exception("Video unavailable")
        mock_api_class.return_value = mock_api_instance

        with pytest.raises(NoTranscriptAvailableError, match="No transcript available"):
            get_transcript("https://youtu.be/test123")

