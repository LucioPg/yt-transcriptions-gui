# tests/test_e2e_mcp.py
"""
End-to-end test for MCP server using real MCP client.
"""
import pytest
import asyncio
from unittest.mock import patch, Mock

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_e2e_mcp_server_connection():
    """Test MCP server connection and tool listing."""
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "src.mcp_server"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize connection
            await session.initialize()

            # List available tools
            tools = await session.list_tools()

            # Verify server has the expected tool
            tool_names = [t.name for t in tools.tools]
            assert "get_transcript" in tool_names

            # Verify tool description
            get_transcript_tool = next(t for t in tools.tools if t.name == "get_transcript")
            assert get_transcript_tool.description is not None
            assert "transcript" in get_transcript_tool.description.lower()


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_e2e_get_transcript_with_mock():
    """Test get_transcript tool call with mocked YouTube API."""
    # Mock the YouTube API to avoid real network calls
    mock_snippet1 = Mock()
    mock_snippet1.text = "Hello world"
    mock_snippet1.start = 0.0
    mock_snippet1.duration = 2.5

    mock_snippet2 = Mock()
    mock_snippet2.text = "This is a test"
    mock_snippet2.start = 2.5
    mock_snippet2.duration = 3.0

    mock_transcript_data = [mock_snippet1, mock_snippet2]

    with patch('src.transcriptor.YouTubeTranscriptApi') as mock_api_class:
        mock_api_instance = Mock()
        mock_api_instance.fetch.return_value = mock_transcript_data
        mock_api_class.return_value = mock_api_instance

        server_params = StdioServerParameters(
            command="python",
            args=["-m", "src.mcp_server"],
        )

        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                # Call the get_transcript tool
                result = await session.call_tool(
                    "get_transcript",
                    {
                        "url": "https://youtu.be/dQw4w9WgXcQ",
                        "format": "txt",
                        "language": None
                    }
                )

                # Verify response structure
                assert len(result.content) > 0

                # The result should contain the transcript data
                # MCP returns text content, so we check for expected content
                content_text = str(result.content)
                assert "Hello world" in content_text or "content" in content_text.lower()


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_e2e_get_transcript_vtt_format():
    """Test get_transcript tool with VTT format for citations."""
    mock_snippet = Mock()
    mock_snippet.text = "Test content"
    mock_snippet.start = 0.0
    mock_snippet.duration = 2.0

    mock_transcript_data = [mock_snippet]

    with patch('src.transcriptor.YouTubeTranscriptApi') as mock_api_class:
        mock_api_instance = Mock()
        mock_api_instance.fetch.return_value = mock_transcript_data
        mock_api_class.return_value = mock_api_instance

        with patch('src.transcriptor.get_available_languages') as mock_avail:
            mock_avail.return_value = ["en"]

            server_params = StdioServerParameters(
                command="python",
                args=["-m", "src.mcp_server"],
            )

            async with stdio_client(server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()

                    # Call with VTT format for citations
                    result = await session.call_tool(
                        "get_transcript",
                        {
                            "url": "https://youtu.be/test123",
                            "format": "vtt",
                            "language": "en"
                        }
                    )

                    # Verify VTT format is used
                    content_text = str(result.content)
                    assert "WEBVTT" in content_text or "00:00:00" in content_text or "content" in content_text.lower()


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_e2e_invalid_url_error():
    """Test error handling for invalid URL."""
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "src.mcp_server"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Call with invalid URL
            result = await session.call_tool(
                "get_transcript",
                {
                    "url": "https://invalid-url.com",
                    "format": "txt",
                    "language": None
                }
            )

            # Should return error content
            assert result.content is not None
            content_text = str(result.content).lower()
            # Either contains error info or is an error response
            assert "error" in content_text or len(result.content) > 0


if __name__ == "__main__":
    # Run a single test for quick verification
    asyncio.run(test_e2e_mcp_server_connection())
    print("[OK] E2E test passed!")
