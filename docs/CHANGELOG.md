# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Web interface documentation with comprehensive coverage
- Updated API documentation to include FastAPI endpoints
- Enhanced architecture documentation for dual-interface system
- Web development patterns and guidelines
- Updated project structure documentation

### Changed
- Improved documentation structure for better navigation
- Updated development setup instructions
- Enhanced project overview with dual-interface features

## [0.2.0] - 2025-11-18

### Added
- **Web Interface**: Complete FastAPI-based web application
  - Responsive HTML interface with Pico.css styling
  - Italian language interface for enhanced accessibility
  - Real-time transcript preview and download functionality
  - Form-based URL input with format selection
  - File download system with temporary file management
  - Comprehensive error handling with user-friendly messages
  - Health check endpoint for monitoring

- **Web API Endpoints**:
  - `GET /`: Homepage with extraction form
  - `POST /extract`: Process transcript extraction from form data
  - `GET /download/{filename}`: Secure file download endpoint
  - `GET /health`: Health check endpoint for monitoring

- **Template System**:
  - `base.html`: Base layout with Pico.css and responsive design
  - `index.html`: Homepage with extraction form and instructions
  - `result.html`: Results display with transcript preview and downloads

- **Web Dependencies**:
  - `fastapi>=0.121.2`: Modern web framework
  - `jinja2>=3.1.6`: Template engine for HTML rendering
  - `python-multipart>=0.0.20`: Form data processing
  - `uvicorn>=0.38.0`: ASGI server for FastAPI
  - `httpx>=0.28.1`: HTTP client for testing

- **Documentation**:
  - Complete web interface documentation (WEB_INTERFACE.md)
  - Updated API documentation with FastAPI endpoints
  - Enhanced architecture documentation for dual-interface system
  - Web development patterns and guidelines

### Changed
- **Dual Interface Architecture**: Refactored to support both CLI and web interfaces
  - Shared core functionality between interfaces
  - Consistent behavior across all access methods
  - Enhanced error handling for both interfaces

- **Dependencies**: Updated to include web framework requirements
- **Project Structure**: Added templates and static files directories
- **Testing**: Extended test coverage for web interface components

### Features
- **User Experience**: Intuitive web interface for non-technical users
- **Accessibility**: Italian language interface and responsive design
- **Performance**: FastAPI async framework for high performance
- **Security**: Secure file handling and path validation
- **Monitoring**: Health check endpoint for deployment monitoring

### Technical Details
- **Framework**: FastAPI with automatic OpenAPI documentation
- **Styling**: Pico.css for minimal, responsive design
- **Templates**: Jinja2 with secure template rendering
- **File Management**: Secure temporary file handling with cleanup
- **Error Handling**: Comprehensive error management with user guidance

### Web Interface Usage
```bash
# Start web interface
uv run python -m src.web_app

# Access at http://localhost:8000
# API documentation at http://localhost:8000/docs
# Health check at http://localhost:8000/health
```

### Web Testing
```bash
# Run web interface tests
uv run python -m pytest tests/test_web_app.py

# Test with coverage
uv run python -m pytest tests/test_web_app.py --cov=src.web_app
```

### Deployment Ready
- Docker support with multi-stage builds
- Production-ready configuration
- Environment variable support
- Health check endpoints for load balancers
- Secure file handling for production environments

### Changed
- Improved error handling and validation
- Enhanced file naming conflict resolution
- Better cross-platform compatibility

### Fixed
- File encoding issues with international characters
- URL validation for edge cases
- Filename sanitization for special characters

## [0.1.0] - 2025-11-18

### Added
- Initial release of YouTube Transcriptor CLI tool
- Core transcript extraction functionality
- Support for multiple output formats (TXT, SRT, VTT)
- Language preference selection
- Automatic filename generation from video title
- Command-line interface with argument parsing
- Comprehensive test suite with 88% coverage
- File handling with conflict resolution
- YouTube URL validation and video ID extraction
- Cross-platform file path handling

### Features
- **CLI Interface**: Professional command-line tool with helpful usage examples
- **Multi-format Support**: Export transcripts in TXT, SRT, or VTT formats
- **Language Selection**: Choose specific languages or use auto-detection
- **File Management**: Automatic file naming and conflict resolution
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Cross-platform**: Works on Windows, macOS, and Linux

### Technical Details
- **Python 3.13+**: Modern Python with latest language features
- **uv Package Manager**: Fast dependency management
- **pytest Testing**: Comprehensive test suite with mocking
- **Type Hints**: Full type annotation support
- **PEP 8 Compliance**: Clean, readable code following Python standards

### Dependencies
- `youtube-transcript-api>=1.2.3` - Core transcript extraction
- `pytest>=9.0.1` - Testing framework (dev dependency)
- `coverage>=7.12.0` - Code coverage measurement (dev dependency)

### Project Structure
```
yt-transcriptor/
├── src/                     # Source code
│   ├── main.py             # CLI interface
│   ├── transcriptor.py     # Core logic
│   ├── file_handler.py     # File operations
│   └── utils.py            # Utilities
├── tests/                  # Test suite
├── docs/                   # Documentation
└── transcriptions/         # Default output directory
```

### CLI Usage Examples

```bash
# Basic usage
uv run python -m src.main "https://www.youtube.com/watch?v=VIDEO_ID"

# With options
uv run python -m src.main "https://www.youtube.com/watch?v=VIDEO_ID" \
  --format srt \
  --language en \
  --output ./transcripts

# Help
uv run python -m src.main --help
```

### Supported Output Formats

**TXT Format**
- Plain text transcript
- Clean, readable format
- Suitable for documentation

**SRT Format**
- Subtitle format with timestamps
- Compatible with video players
- Standard subtitle format

**VTT Format**
- Web Video Text Tracks
- Browser-compatible
- Modern web standard

### Error Handling

- **Invalid URLs**: Clear validation and error messages
- **Missing Transcripts**: Graceful handling when no transcript is available
- **Network Issues**: Timeout and connection error handling
- **File System**: Permission and disk space error handling

### Testing Coverage

- **Unit Tests**: Individual function testing with comprehensive mocking
- **Integration Tests**: End-to-end workflow verification
- **CLI Tests**: Command-line interface testing
- **Error Case Tests**: Comprehensive error condition coverage

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/yt-transcriptor.git
cd yt-transcriptor

# Set up environment
uv sync

# Run tests
uv run python -m pytest tests/

# Use the tool
uv run python -m src.main "https://www.youtube.com/watch?v=VIDEO_ID"
```

## Development Notes

### Code Quality
- 88% test coverage
- Full type annotation
- Comprehensive documentation
- PEP 8 compliant code
- Modern Python practices

### Future Enhancements
- Web interface option
- Batch processing capabilities
- Additional output formats
- Transcript caching
- Search functionality
- Integration with other platforms

### Known Limitations
- Single video processing (no batch mode)
- No local caching mechanism
- Limited to YouTube platform
- Basic video title extraction

---

## Version History

### v0.1.0 (2025-11-18)
- Initial public release
- Core functionality complete
- Comprehensive documentation
- Full test coverage

### Development Milestones
- **Project Setup**: Environment configuration and dependencies
- **Core Logic**: Transcript extraction and API integration
- **File Operations**: Output formatting and file management
- **CLI Interface**: Command-line tool development
- **Testing**: Comprehensive test suite implementation
- **Documentation**: User and developer documentation
- **Release**: Package preparation and publication

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines.

### Contributors
- Initial development by the project team
- Community contributions welcome

### License

This project is for educational and personal use. See LICENSE file for details.

---

## Support

- **Issues**: Report bugs via GitHub Issues
- **Features**: Request features via GitHub Discussions
- **Documentation**: See docs/ directory for detailed guides
- **Testing**: Run `pytest` for verification

---

*Last updated: 2025-11-18*