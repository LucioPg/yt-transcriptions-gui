# tests/test_mcp_server.py
"""
Tests for MCP server implementation.
"""
import pytest
from unittest.mock import Mock, patch, create_autospec


def test_get_transcript_tool_success():
    """Test successful transcript extraction via MCP tool."""
    from src.mcp_server import get_transcript, TranscriptResult
    from src.transcriptor import NoTranscriptAvailableError, InvalidVideoURLError
    from youtube_transcript_api import YouTubeTranscriptApi

    # Mock transcript data as returned by YouTubeTranscriptApi.fetch()
    mock_snippet1 = Mock()
    mock_snippet1.text = "Hello world"
    mock_snippet1.start = 0.0
    mock_snippet1.duration = 2.5

    mock_snippet2 = Mock()
    mock_snippet2.text = "This is a test"
    mock_snippet2.start = 2.5
    mock_snippet2.duration = 3.0

    mock_transcript_data = [mock_snippet1, mock_snippet2]

    with patch('src.mcp_server.get_transcript') as mock_get:
        mock_get.return_value = mock_transcript_data

        with patch('src.mcp_server.get_video_title') as mock_title:
            mock_title.return_value = "Test Video Title"

            with patch('src.mcp_server.format_transcript') as mock_format:
                mock_format.return_value = "Hello world\nThis is a test"

                result = get_transcript(
                    url="https://youtu.be/test123",
                    format="txt",
                    language=None
                )

                assert isinstance(result, TranscriptResult)
                assert result.video_url == "https://youtu.be/test123"
                assert result.video_title == "Test Video Title"
                assert result.content == "Hello world\nThis is a test"
                assert result.format == "txt"
                assert result.segments_count == 2


def test_get_transcript_tool_vtt_format():
    """Test transcript extraction with VTT format for citations."""
    from src.mcp_server import get_transcript, TranscriptResult

    # Mock transcript data
    mock_snippet = Mock()
    mock_snippet.text = "Test content"
    mock_snippet.start = 0.0
    mock_snippet.duration = 2.0

    mock_transcript_data = [mock_snippet]

    with patch('src.mcp_server.get_transcript') as mock_get:
        mock_get.return_value = mock_transcript_data

        with patch('src.mcp_server.get_video_title') as mock_title:
            mock_title.return_value = "Test Video"

            with patch('src.mcp_server.format_transcript') as mock_format:
                vtt_content = "WEBVTT\n\n00:00:00.000 --> 00:00:02.000\nTest content\n"
                mock_format.return_value = vtt_content

                result = get_transcript(
                    url="https://youtu.be/test123",
                    format="vtt",
                    language="en"
                )

                assert result.format == "vtt"
                assert result.content == vtt_content
                assert result.language == "en"
                mock_format.assert_called_once_with(mock_transcript_data, "vtt")


def test_get_transcript_tool_invalid_url():
    """Test error handling for invalid URLs."""
    from src.mcp_server import get_transcript
    from src.transcriptor import InvalidVideoURLError

    with patch('src.mcp_server.get_transcript') as mock_get:
        mock_get.side_effect = InvalidVideoURLError("Invalid YouTube URL: https://google.com")

        with pytest.raises(InvalidVideoURLError, match="Invalid YouTube URL"):
            get_transcript(url="https://google.com", format="txt", language=None)


def test_get_transcript_tool_no_transcript_available():
    """Test error handling when no transcript is available."""
    from src.mcp_server import get_transcript
    from src.transcriptor import NoTranscriptAvailableError

    with patch('src.mcp_server.get_transcript') as mock_get:
        mock_get.side_effect = NoTranscriptAvailableError("No transcript available")

        with pytest.raises(NoTranscriptAvailableError, match="No transcript available"):
            get_transcript(
                url="https://youtu.be/notranscript",
                format="txt",
                language=None
            )


def test_get_available_languages():
    """Test get_available_languages function."""
    from src.transcriptor import get_available_languages

    # Mock transcript list with language codes
    mock_transcript1 = Mock()
    mock_transcript1.language_code = "en"

    mock_transcript2 = Mock()
    mock_transcript2.language_code = "it"

    mock_transcript3 = Mock()
    mock_transcript3.language_code = "es"

    # Mock the list_transcripts result
    mock_list = Mock()
    mock_list.__iter__ = Mock(return_value=iter([mock_transcript1, mock_transcript2, mock_transcript3]))

    with patch('src.transcriptor.YouTubeTranscriptApi') as mock_api_class:
        mock_api_instance = Mock()
        mock_api_instance.list_transcripts.return_value = mock_list
        mock_api_class.return_value = mock_api_instance

        result = get_available_languages("https://youtu.be/test123")

        assert result == ["en", "it", "es"]
        mock_api_instance.list_transcripts.assert_called_once_with("test123")


def test_get_available_languages_error_returns_empty():
    """Test that get_available_languages returns empty list on error."""
    from src.transcriptor import get_available_languages

    with patch('src.transcriptor.YouTubeTranscriptApi') as mock_api_class:
        mock_api_instance = Mock()
        mock_api_instance.list_transcripts.side_effect = Exception("API Error")
        mock_api_class.return_value = mock_api_instance

        result = get_available_languages("https://youtu.be/test123")

        # Should return empty list for graceful degradation
        assert result == []


def test_language_fallback_en_to_it():
    """Test language fallback when EN unavailable but IT is."""
    from src.transcriptor import get_transcript
    from youtube_transcript_api import YouTubeTranscriptApi

    # Mock Italian transcript
    mock_snippet = Mock()
    mock_snippet.text = "Contenuto italiano"
    mock_snippet.start = 0.0
    mock_snippet.duration = 2.0

    mock_transcript_data = [mock_snippet]

    with patch('src.transcriptor.YouTubeTranscriptApi') as mock_api_class:
        mock_api_instance = create_autospec(YouTubeTranscriptApi)
        # Simulate: 'de' fails, get_available_languages returns ['it'], 'it' succeeds
        mock_api_instance.fetch.side_effect = [
            Exception("Language not found"),  # 'de' fails
            mock_transcript_data  # 'it' succeeds
        ]
        mock_api_class.return_value = mock_api_instance

        with patch('src.transcriptor.get_available_languages') as mock_avail:
            mock_avail.return_value = ["it", "es"]

            result = get_transcript("https://youtu.be/test123", language="de")

            assert len(result) == 1
            assert result[0].text == "Contenuto italiano"
            # Should have tried 'de' and 'it'
            assert mock_api_instance.fetch.call_count == 2


def test_language_fallback_all_preferred_fail():
    """Test falling back to first available when no preferred language matches."""
    from src.transcriptor import get_transcript
    from youtube_transcript_api import YouTubeTranscriptApi

    # Mock transcript in French (not preferred)
    mock_snippet = Mock()
    mock_snippet.text = "Contenu français"
    mock_snippet.start = 0.0
    mock_snippet.duration = 2.0

    mock_transcript_data = [mock_snippet]

    with patch('src.transcriptor.YouTubeTranscriptApi') as mock_api_class:
        mock_api_instance = Mock()
        # Only French available (fallback call)
        mock_api_instance.fetch.return_value = mock_transcript_data
        mock_api_class.return_value = mock_api_instance

        with patch('src.transcriptor.get_available_languages') as mock_avail:
            # Available languages don't include preferred ones (en, it)
            mock_avail.return_value = ["fr", "de"]

            result = get_transcript("https://youtu.be/test123")

            assert len(result) == 1
            assert result[0].text == "Contenu français"
            # Since no preferred language is available, only 1 call is made (fallback)
            assert mock_api_instance.fetch.call_count == 1
            # Verify it was called without specific language (fallback)
            mock_api_instance.fetch.assert_called_once_with("test123")


def test_transcript_result_model():
    """Test TranscriptResult Pydantic model validation."""
    from src.mcp_server import TranscriptResult

    result = TranscriptResult(
        video_url="https://youtu.be/test123",
        video_title="Test Video",
        content="Test content",
        language="en",
        format="txt",
        segments_count=5
    )

    assert result.video_url == "https://youtu.be/test123"
    assert result.video_title == "Test Video"
    assert result.content == "Test content"
    assert result.language == "en"
    assert result.format == "txt"
    assert result.segments_count == 5
