# YouTube Transcriptor

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![Test Coverage](https://img.shields.io/badge/coverage-88%25-green.svg)](htmlcov/index.html)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A lightweight, professional Python tool that extracts YouTube video transcripts directly without downloading videos. Features both CLI and web interfaces, built with modern Python practices and comprehensive testing.

## ✨ Features

- 🎯 **Direct Transcript Extraction**: Download transcripts without video downloads
- 🌐 **Dual Interface**: Both CLI and web interface for different use cases
- 📝 **Multiple Output Formats**: Support for TXT, SRT, and VTT formats
- 🌍 **Language Selection**: Manual language override or auto-detection
- 📁 **Smart File Management**: Automatic filename generation and conflict resolution
- 🎨 **Clean Web Design**: Minimal, responsive interface using Pico.css
- ⚡ **High Performance**: Fast extraction with minimal resource usage
- 🔧 **Developer Friendly**: Extensive test coverage and clean architecture
- 🛡️ **Robust Error Handling**: Comprehensive error handling with user-friendly messages

## 🚀 Quick Start

### Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) package manager (recommended)

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/yt-transcriptor.git
cd yt-transcriptor

# Set up the environment
uv sync

# Verify installation
uv run python -m pytest tests/
```

## 📖 Usage

### Web Interface (Recommended)

Start the web interface for a user-friendly experience:

```bash
# Start the web server
uv run python -m src.web_app

# Then open your browser to http://localhost:8000
```

The web interface provides:
- 🎨 Clean, responsive design
- 📝 Real-time transcript preview
- 💾 Direct download in multiple formats
- 🌍 Language selection
- ❌ User-friendly error messages

### CLI Usage

#### Basic Usage

```bash
# Extract transcript in default format (TXT)
uv run python -m src.main "https://www.youtube.com/watch?v=VIDEO_ID"
```

#### Advanced Usage

```bash
# Extract with custom options
uv run python -m src.main "https://www.youtube.com/watch?v=VIDEO_ID" \
  --format srt \
  --language en \
  --output ./transcripts
```

### Command Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--format` | `-f` | Output format (txt, srt, vtt) | `txt` |
| `--language` | `-l` | Language code (en, it, es, etc.) | auto-detect |
| `--output` | `-o` | Output directory | `transcriptions` |

### Examples

```bash
# Plain text transcript (default)
uv run python -m src.main "https://youtu.be/dQw4w9WgXcQ"

# SRT subtitles in English
uv run python -m src.main "https://youtu.be/dQw4w9WgXcQ" --format srt --language en

# VTT format with custom output directory
uv run python -m src.main "https://youtu.be/dQw4w9WgXcQ" --format vtt --output ./subtitles

# Using short options
uv run python -m src.main "https://youtu.be/dQw4w9WgXcQ" -f srt -l en -o ./output
```

## 📁 Output Formats

### TXT Format
Plain text transcript suitable for reading and documentation.

```
Hello world, this is a transcript example.
This is the second line of the transcript.
```

### SRT Format
Standard subtitle format compatible with video players.

```srt
1
00:00:00,000 --> 00:00:02,500
Hello world, this is a transcript example.

2
00:00:02,500 --> 00:00:05,000
This is the second line of the transcript.
```

### VTT Format
Web Video Text Tracks format for web applications.

```vtt
WEBVTT

00:00:00.000 --> 00:00:02.500
Hello world, this is a transcript example.

00:00:02.500 --> 00:00:05.000
This is the second line of the transcript.
```

## 🏗️ Architecture

```
YouTube Transcriptor
├── CLI Interface (main.py)
├── Core Logic (transcriptor.py)
├── File Operations (file_handler.py)
└── Utilities (utils.py)
```

### Key Components

- **main.py**: Command-line interface and user interaction
- **transcriptor.py**: YouTube API integration and transcript extraction
- **file_handler.py**: File operations and output formatting
- **utils.py**: URL validation and text processing

## 🧪 Testing

```bash
# Run all tests
uv run python -m pytest tests/

# Run with coverage report
uv run python -m pytest tests/ --cov=src --cov-report=html

# Run specific test file
uv run python -m pytest tests/test_transcriptor.py

# Verbose output
uv run python -m pytest tests/ -v
```

### Test Coverage

- **Overall Coverage**: 88%
- **Unit Tests**: Individual function testing with mocking
- **Integration Tests**: End-to-end workflow verification
- **CLI Tests**: Command-line interface testing

## 🛠️ Development

### Development Setup

```bash
# Install development dependencies
uv sync --extra dev

# Run tests
uv run python -m pytest tests/

# Check code style
black src/ tests/
flake8 src/ tests/

# Build package
python -m build
```

### Project Structure

```
yt-transcriptor/
├── src/                     # Source code
│   ├── main.py             # CLI interface
│   ├── transcriptor.py     # Core transcript extraction
│   ├── file_handler.py     # File operations and formatting
│   └── utils.py            # Utility functions
├── tests/                  # Test suite
│   ├── test_main.py        # CLI tests
│   ├── test_transcriptor.py # Core logic tests
│   ├── test_file_handler.py # File operations tests
│   ├── test_utils.py       # Utility tests
│   └── test_integration.py # End-to-end tests
├── docs/                   # Documentation
│   ├── API.md              # API documentation
│   ├── ARCHITECTURE.md     # System architecture
│   ├── CONTRIBUTING.md     # Contribution guidelines
│   ├── DEVELOPMENT.md      # Development guide
│   └── CHANGELOG.md        # Version history
├── htmlcov/               # Coverage reports
└── transcriptions/        # Default output directory
```

## 📚 Documentation

- [API Documentation](docs/API.md) - Detailed API reference
- [Architecture Guide](docs/ARCHITECTURE.md) - System design and architecture
- [Development Guide](docs/DEVELOPMENT.md) - Development setup and guidelines
- [Contributing Guidelines](docs/CONTRIBUTING.md) - How to contribute to the project
- [Changelog](docs/CHANGELOG.md) - Version history and changes

## 🔧 Dependencies

### Runtime Dependencies
- **Python 3.13+**: Modern Python with latest language features
- **youtube-transcript-api**: YouTube transcript extraction library

### Development Dependencies
- **pytest**: Testing framework with powerful features
- **coverage**: Code coverage measurement
- **black**: Code formatting
- **flake8**: Code linting

### Build Dependencies
- **hatchling**: Build system for package distribution

## 🌍 Supported URL Formats

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`

## ⚠️ Error Handling

The tool provides comprehensive error handling for common issues:

- **Invalid URLs**: Clear validation and helpful error messages
- **Missing Transcripts**: Graceful handling when no transcript is available
- **Network Issues**: Timeout and connection error handling
- **File System**: Permission and disk space error handling
- **Language Issues**: Fallback handling for unavailable languages

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](docs/CONTRIBUTING.md) for detailed information on how to get started.

### Quick Contribution Steps

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: Report bugs via [GitHub Issues](https://github.com/your-username/yt-transcriptor/issues)
- **Features**: Request features via [GitHub Discussions](https://github.com/your-username/yt-transcriptor/discussions)
- **Documentation**: See [docs/](docs/) directory for detailed guides

## 🙏 Acknowledgments

- [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) for the core transcript extraction functionality
- The Python community for excellent tools and libraries

---

**Note**: This tool is for educational and personal use. Please respect YouTube's Terms of Service and copyright laws when using extracted transcripts.
