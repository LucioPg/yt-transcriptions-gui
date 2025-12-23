# Contributing to YouTube Transcriptions GUI

Thank you for your interest in contributing to YouTube Transcriptions GUI! This document provides guidelines and instructions for contributors.

## Table of Contents

- [Development Setup](#development-setup)
- [Code Style and Conventions](#code-style-and-conventions)
- [Testing Guidelines](#testing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Bug Reports](#bug-reports)
- [Feature Requests](#feature-requests)

## Development Setup

### Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) package manager

### Getting Started

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/LucioPG/yt-transcriptions-gui.git
   cd yt-transcriptions-gui
   ```

2. **Set up the development environment**
   ```bash
   uv sync
   ```

3. **Install development dependencies**
   ```bash
   uv sync --dev
   ```

4. **Verify the setup**
   ```bash
   uv run python -m pytest tests/
   ```

### Running the Application

```bash
# Run from source
uv run python -m src.main "https://www.youtube.com/watch?v=VIDEO_ID"

# Run with CLI script
uv run yt-transcriptor "https://www.youtube.com/watch?v=VIDEO_ID"
```

## Code Style and Conventions

### Python Code Style

- Follow [PEP 8](https://pep8.org/) guidelines
- Use [Black](https://black.readthedocs.io/) for code formatting
- Maximum line length: 88 characters
- Use type hints for function signatures

### Documentation Style

- Use docstrings for all public functions and classes
- Follow the Google Python Style Guide for docstrings
- Include type hints in docstrings

```python
def example_function(param1: str, param2: int) -> bool:
    """Example function with proper documentation.

    Args:
        param1: Description of first parameter
        param2: Description of second parameter

    Returns:
        Description of return value

    Raises:
        ValueError: When invalid input is provided
    """
    pass
```

### Import Organization

- Group imports in the following order:
  1. Standard library imports
  2. Third-party imports
  3. Local application imports
- Use absolute imports for local modules

### Naming Conventions

- Use `snake_case` for functions and variables
- Use `PascalCase` for classes
- Use `UPPER_CASE` for constants
- Be descriptive with names

## Testing Guidelines

### Test Coverage

- Aim for 95%+ test coverage
- All public functions must have tests
- Test both success and failure cases

### Testing Structure

```
tests/
├── unit/           # Unit tests for individual modules
├── integration/    # Integration tests
└── fixtures/       # Test data and mocks
```

### Writing Tests

- Use `pytest` for all tests
- Use descriptive test names that explain what is being tested
- Use fixtures for setup and teardown
- Mock external dependencies

```python
def test_get_transcript_success():
    """Test successful transcript extraction."""
    from src.transcriptor import get_transcript

    with patch('src.transcriptor.YouTubeTranscriptApi') as mock_api:
        mock_transcript = [
            {'text': 'Hello world', 'start': 0.0, 'duration': 2.5}
        ]
        mock_api.get_transcript.return_value = mock_transcript

        result = get_transcript("https://youtu.be/test123")

        assert result == mock_transcript
        mock_api.get_transcript.assert_called_once()
```

### Running Tests

```bash
# Run all tests
uv run python -m pytest tests/

# Run with coverage
uv run python -m pytest tests/ --cov=src --cov-report=html

# Run specific test file
uv run python -m pytest tests/test_transcriptor.py

# Run with verbose output
uv run python -m pytest tests/ -v
```

## Pull Request Process

### Before Submitting

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow coding standards
   - Add tests for new functionality
   - Update documentation if needed

3. **Run the test suite**
   ```bash
   uv run python -m pytest tests/
   ```

4. **Check code coverage**
   ```bash
   uv run python -m pytest tests/ --cov=src --cov-report=html
   ```

### Submitting a Pull Request

1. **Update your fork and create pull request**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Fill out the pull request template**
   - Describe your changes
   - Link to any relevant issues
   - Include screenshots if applicable

3. **Request a code review**

### Pull Request Requirements

- All tests must pass
- Code coverage must not decrease
- Documentation must be updated if applicable
- Code must follow style guidelines

## Bug Reports

### Creating Bug Reports

1. **Use the bug report template**
2. **Provide clear, descriptive title**
3. **Include reproduction steps**
4. **Add system information**
5. **Include error messages and logs**

### Bug Report Template

```markdown
## Bug Description
Brief description of the bug

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., Windows 10, macOS 12.0, Ubuntu 20.04]
- Python version: [e.g., 3.13.0]
- Package version: [e.g., 0.1.0]

## Additional Context
Any other relevant information
```

## Feature Requests

### Requesting Features

1. **Check existing issues** first
2. **Use the feature request template**
3. **Describe the problem** you're trying to solve
4. **Propose a solution** if you have one

### Feature Request Template

```markdown
## Feature Description
Clear description of the feature

## Problem Statement
What problem does this feature solve?

## Proposed Solution
How should this feature work?

## Alternatives Considered
Other approaches you've thought about

## Additional Context
Any other relevant information
```

## Getting Help

- Check the [documentation](../README.md)
- Search existing [issues](https://github.com/your-username/yt-transcriptor/issues)
- Join our discussions (if available)

## License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project.