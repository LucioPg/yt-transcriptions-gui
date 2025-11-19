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

- Python 3.13+ (for development)
- [uv](https://github.com/astral-sh/uv) package manager (recommended)
- Windows (for executables)
- Rust toolchain and npm (for Tauri desktop app)

### Installation Options

#### Option 1: Download Executables (Recommended for Users)

Download the pre-built executables from the [Releases](https://github.com/your-username/yt-transcriptor/releases) page:

- **yt-transcriptor-desktop.exe** - Native desktop application (Tauri)
- **yt-transcriptor-cli.exe** - Command-line interface for advanced users

#### Option 2: Development Setup

```bash
# Clone the repository
git clone https://github.com/your-username/yt-transcriptor.git
cd yt-transcriptor

# Set up the environment
uv sync

# Verify installation
uv run python -m pytest tests/

# Build executables (optional)
make build-all-exe
```

## 📖 Usage

### Windows Executables (Recommended)

#### Desktop Application - yt-transcriptor-desktop.exe

Perfect for everyday users with a native desktop experience:

```bash
# Run the desktop application (completely self-contained)
yt-transcriptor-desktop.exe

# The application will:
# - Start Python backend automatically
# - Launch in a native desktop window
# - Find available ports dynamically
# - Handle all internal process management
```

The desktop application provides:
- 🎨 Native desktop window (1000x800)
- 📝 Real-time transcript preview
- 💾 Direct download functionality
- 🌍 Language selection
- ❌ User-friendly error messages
- ⚡ Automatic backend management
- 🔧 No external dependencies required

#### CLI Interface - yt-transcriptor-cli.exe

For power users and automation:

```bash
# Basic usage
yt-transcriptor-cli.exe "https://www.youtube.com/watch?v=VIDEO_ID"

# Advanced usage
yt-transcriptor-cli.exe "https://www.youtube.com/watch?v=VIDEO_ID" \
  --format srt \
  --language en \
  --output ./transcripts

# Help
yt-transcriptor-cli.exe --help
```

### Development Mode

#### Web Interface (Development)

```bash
# Start the web server in development mode
uv run python -m src.web_main

# Then open your browser to http://localhost:8000
# Note: This uses temporary files, not ~/yt-transcriptions/
```

#### CLI Interface (Development)

```bash
# Basic usage
uv run python -m src.cli_main "https://www.youtube.com/watch?v=VIDEO_ID"

# Advanced usage
uv run python -m src.cli_main "https://www.youtube.com/watch?v=VIDEO_ID" \
  --format srt \
  --language en \
  --output ./transcripts
```

### CLI Command Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--format` | `-f` | Output format (txt, srt, vtt) | `txt` |
| `--language` | `-l` | Language code (en, it, es, etc.) | auto-detect |
| `--output` | `-o` | Output directory | `transcriptions` |

### Examples

#### Windows Executables

```bash
# Plain text transcript (default)
yt-transcriptor-cli.exe "https://youtu.be/dQw4w9WgXcQ"

# SRT subtitles in English
yt-transcriptor-cli.exe "https://youtu.be/dQw4w9WgXcQ" --format srt --language en

# VTT format with custom output directory
yt-transcriptor-cli.exe "https://youtu.be/dQw4w9WgXcQ" --format vtt --output ./subtitles

# Using short options
yt-transcriptor-cli.exe "https://youtu.be/dQw4w9WgXcQ" -f srt -l en -o ./output
```

#### Development Mode

```bash
# Plain text transcript (default)
uv run python -m src.cli_main "https://youtu.be/dQw4w9WgXcQ"

# SRT subtitles in English
uv run python -m src.cli_main "https://youtu.be/dQw4w9WgXcQ" --format srt --language en

# VTT format with custom output directory
uv run python -m src.cli_main "https://youtu.be/dQw4w9WgXcQ" --format vtt --output ./subtitles

# Using short options
uv run python -m src.cli_main "https://youtu.be/dQw4w9WgXcQ" -f srt -l en -o ./output
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

## 🏗️ Dual-Interface Architecture

The YouTube Transcriptor features a dual-interface architecture designed for different user needs:

### Architecture Overview

```
YouTube Transcriptor
├── CLI Executable (yt-transcriptor-cli.exe)
│   └── Console interface for power users
├── Desktop Application (yt-transcriptor-desktop.exe)
│   └── Self-contained native app with integrated backend
└── Shared Core Logic
    ├── transcriptor.py: YouTube API integration
    ├── file_handler.py: File operations
    ├── utils.py: Utilities and validation
    └── web_app.py: FastAPI web framework
```

### Executable Details

#### yt-transcriptor-cli.exe
- **Purpose**: Command-line interface for advanced users
- **Target**: Developers, power users, automation scripts
- **Output**: User-specified directory
- **Interface**: Console with full argument support

#### yt-transcriptor-desktop.exe (Tauri Application)
- **Purpose**: Self-contained native desktop application
- **Target**: Everyday users who prefer desktop apps
- **Output**: User-selected directory via download functionality
- **Interface**: Native window (1000x800) with embedded web interface
- **Backend**: Integrated Python backend managed automatically

### Key Components

- **cli_main.py**: CLI entry point and argument parsing
- **web_main.py**: Web executable entry point
- **transcriptor.py**: YouTube API integration and transcript extraction
- **file_handler.py**: File operations and output formatting
- **utils.py**: URL validation and text processing
- **web_app.py**: FastAPI web interface
- **templates/**: HTML templates for web interface
- **static/**: CSS, JavaScript, and image assets

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

### Building Windows Executables

#### Prerequisites
- Windows operating system
- Python 3.13+ with uv package manager

#### Build Both Executables
```bash
# Build both CLI and web executables
make build-all-exe

# Or build individually
make build-cli-exe    # Builds yt-transcriptor-cli.exe
make build-web-exe    # Builds yt-transcriptor-web.exe
```

#### Manual Build Process
```bash
# Install packaging dependencies
uv sync --extra packaging

# Build CLI executable
uv run pyinstaller --onefile --console --name "yt-transcriptor-cli" src/cli_main.py

# Build Web executable
uv run pyinstaller --onefile --windowed \
  --add-data "src/templates;templates" \
  --add-data "src/static;static" \
  --name "yt-transcriptor-web" \
  src/web_main.py
```

#### Executable Output
- CLI executable: `dist/yt-transcriptor-cli.exe`
- Web executable: `dist/yt-transcriptor-web.exe`

#### Test Executables
```bash
# Test CLI executable
dist/yt-transcriptor-cli.exe --help

# Test web executable (requires manual run)
dist/yt-transcriptor-web.exe
```

### Project Structure

```
yt-transcriptor/
├── src/                     # Source code
│   ├── cli_main.py         # CLI executable entry point
│   ├── web_main.py         # Web executable entry point
│   ├── main.py             # Legacy CLI interface (development)
│   ├── transcriptor.py     # Core transcript extraction
│   ├── file_handler.py     # File operations and formatting
│   ├── utils.py            # Utility functions
│   ├── web_app.py          # FastAPI web interface (development)
│   ├── setup.py            # Package setup
│   ├── templates/          # HTML templates for web interface
│   │   ├── base.html       # Base layout with styling
│   │   ├── index.html      # Homepage with extraction form
│   │   └── result.html     # Results display page
│   └── static/             # Static files (CSS, JS, images)
├── src-tauri/              # Tauri desktop application
│   ├── src/main.rs         # Rust main application with backend management
│   ├── Cargo.toml          # Rust dependencies
│   └── tauri.conf.json     # Tauri configuration
├── web-dist/               # Static web assets for Tauri
│   └── index.html          # Embedded web interface
├── tests/                  # Test suite
│   ├── test_main.py        # Legacy CLI tests
│   ├── test_transcriptor.py # Core logic tests
│   ├── test_file_handler.py # File operations tests
│   ├── test_utils.py       # Utility tests
│   ├── test_web_app.py     # Web interface tests
│   └── test_integration.py # End-to-end tests
├── docs/                   # Documentation
│   ├── API.md              # API documentation (CLI + Web)
│   ├── ARCHITECTURE.md     # System architecture
│   ├── TAURI_DESKTOP_APP.md # Tauri desktop application guide
│   ├── CONTRIBUTING.md     # Contribution guidelines
│   ├── DEVELOPMENT.md      # Development guide
│   └── CHANGELOG.md        # Version history
├── dist/                   # Built executables
│   ├── yt-transcriptor-cli.exe    # CLI Windows executable
│   └── yt-transcriptor-desktop.exe # Desktop application (Tauri)
├── htmlcov/               # Coverage reports
├── transcriptions/        # Default CLI output directory
└── yt-transcriptor-cli.spec # PyInstaller spec for CLI
```

### Tauri Desktop Application

```bash
# Run Tauri in development mode (backend starts automatically)
npm run tauri:dev

# Build for production (completely self-contained)
npm run tauri:build
```

### Key Differences Between Interfaces

| Feature | yt-transcriptor-cli.exe | yt-transcriptor-desktop.exe |
|---------|------------------------|---------------------------|
| **Target Users** | Developers, power users | Everyday users |
| **Interface** | Console/Command line | Native desktop window |
| **Output Location** | User-specified | User-selected via download |
| **Arguments** | Full CLI argument support | Web form interface |
| **Auto-launch** | No | Native desktop window |
| **File Management** | Manual | User-controlled downloads |
| **Dependencies** | Python runtime | Self-contained (includes Python) |

## 📚 Documentation

### User Documentation
- **[Web Interface Guide](docs/WEB_INTERFACE.md)** - Complete web interface documentation
- **[Tauri Desktop App](docs/TAURI_DESKTOP_APP.md)** - Native desktop application guide
- [API Documentation](docs/API.md) - Detailed API reference including web endpoints
- [Architecture Guide](docs/ARCHITECTURE.md) - System design and triple-interface architecture

### Developer Documentation
- [Development Guide](docs/DEVELOPMENT.md) - Development setup, patterns, and web development
- [Contributing Guidelines](docs/CONTRIBUTING.md) - How to contribute to the project
- [Changelog](docs/CHANGELOG.md) - Version history and changes

### Quick Links

#### Windows Executables
- 🖥️ **Desktop Application**: `yt-transcriptor-desktop.exe` (self-contained)
- 🔧 **CLI Tool**: `yt-transcriptor-cli.exe "https://youtu.be/VIDEO_ID"`

#### Development Mode
- 🖥️ **Desktop App**: `npm run tauri:dev` (starts backend automatically)
- 🔧 **CLI Tool**: `uv run python -m src.cli_main "https://youtu.be/VIDEO_ID"`
- 📖 **Web Interface**: `uv run python -m src.web_main` → http://localhost:8000 (development fallback)

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
