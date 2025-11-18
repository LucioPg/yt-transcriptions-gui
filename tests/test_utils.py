# tests/test_utils.py
def test_validate_youtube_url():
    from src.utils import validate_youtube_url

    # Valid URLs
    assert validate_youtube_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ") == True
    assert validate_youtube_url("https://youtu.be/dQw4w9WgXcQ") == True

    # Invalid URLs
    assert validate_youtube_url("https://www.google.com") == False
    assert validate_youtube_url("not-a-url") == False
    assert validate_youtube_url("") == False

def test_sanitize_filename():
    from src.utils import sanitize_filename

    # Basic sanitization
    assert sanitize_filename("Hello World") == "Hello_World"
    assert sanitize_filename("Hello: World") == "Hello_World"
    assert sanitize_filename('Hello/World\\Test') == "HelloWorldTest"

    # Multiple spaces
    assert sanitize_filename("Hello    World") == "Hello_World"

    # Multiple underscores
    assert sanitize_filename("Hello   World") == "Hello_World"

    # Long titles
    long_title = "A" * 250
    assert len(sanitize_filename(long_title)) <= 200

    # Empty and edge cases
    assert sanitize_filename("") == ""
    assert sanitize_filename("   ") == ""