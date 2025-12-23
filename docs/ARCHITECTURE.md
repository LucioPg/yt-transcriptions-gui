# Architecture Documentation

This document provides an overview of the YouTube Transcriptions GUI architecture, design decisions, and technical implementation details.

## Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Component Design](#component-design)
- [Data Flow](#data-flow)
- [Design Patterns](#design-patterns)
- [Technology Stack](#technology-stack)
- [Security Considerations](#security-considerations)
- [Performance Considerations](#performance-considerations)
- [Scalability Considerations](#scalability-considerations)

## Overview

YouTube Transcriptions GUI is a versatile Python application that provides both CLI and web interfaces for extracting video transcripts directly from YouTube without downloading video content. The system features a dual-interface architecture with a shared core, ensuring consistency across all access methods while providing optimized experiences for different user preferences.

### Key Design Principles

1. **Dual Interface Design**: Separate CLI and web interfaces sharing the same core logic
2. **Modularity**: Clear separation between interfaces, business logic, and utilities
3. **Testability**: Comprehensive testing with mocking for all components
4. **Extensibility**: Easy to add new interfaces, output formats, or features
5. **Robustness**: Graceful error handling and validation across all interfaces
6. **Consistency**: Shared core functionality ensures identical behavior across interfaces
7. **Accessibility**: Web interface provides user-friendly experience for non-technical users

## System Architecture

### High-Level Architecture

```
                 ┌─────────────────────────────────────────────────────────┐
                 │                  YouTube Transcriptions GUI           │
                 │               (Dual-Executable System)                │
                 └─────────────────────────────────────────────────────────┘
                                      │
        ┌─────────────────────────────┼───────────────────────────────────┐
        │                             │                                   │
┌───────▼────────┐          ┌────────▼────────┐              ┌───────────▼──────────┐
│  CLI Executable │          │ Web Executable  │              │     Shared Core       │
│yt-transcriptions  │          │yt-transcriptions  │              │     Modules          │
│   -gui-cli.exe   │          │  -gui-web.exe    │              │                      │
│                │          │                │              ┌────────┴────────┐     │
│                │          │                │              │                 │     │
└───────┬────────┘          └───────┬────────┘              │   Core Logic    │     │
        │                        │                      │                 │     │
        │                        │                      │                 │     │
        ▼                        ▼                ┌─────▼─────┐   ┌─────▼──────┐ │
┌─────────────────┐    ┌─────────────────┐   │ Transcript│   │ File      │ │
│  CLI Interface  │    │  Web Interface  │   │ Processor │   │ Handler   │ │
│  (cli_main.py)  │    │ (web_main.py)   │   │           │   │           │ │
│                 │    │                 │   │           │   │           │ │
│ • Argument      │    │ • FastAPI App   │   │ • YouTube │   │ • File    │ │
│ • Processing    │    │ • Auto Browser  │   │   API     │   │   Ops     │ │
│ • Console       │    │ • Permanent     │   │ • Validation│ │ • Formats │ │
│ • Output        │    │   Downloads     │   │           │   │           │ │
└─────────────────┘    └─────────────────┘   └───────────┘   └───────────┘ │
        │                        │                      │                 │
        └────────────────────────┼──────────────────────┼─────────────────┘
                                 │                      │
                                 ▼                      ▼
                    ┌─────────────────────┐   ┌─────────────────────┐
                    │  Shared Utilities   │   │   Web Resources     │
                    │    (utils.py)        │   │                    │
                    │  - URL Validation    │   │ • Templates/        │
                    │  - Text Processing   │   │ • Static Files/     │
                    │  - Common Functions  │   │ • Auto-launch/      │
                    └─────────────────────┘   └─────────────────────┘
```

### Dual-Executable Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        Core Layer (Shared)                                  │
├─────────────────┬─────────────────┬─────────────────────────────────────────┤
│   transcriptor  │  file_handler   │              utils                     │
│                 │                 │                                     │
│ • get_transcript │ • format_transcript │ • validate_youtube_url          │
│ • get_video_title│ • save_transcript   │ • sanitize_filename              │
│ • API Integration│ • File Operations   │ • Common utilities               │
└─────────────────┴─────────────────┴─────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                   Executable Interface Layer (Separated)                    │
├─────────────────────────────────┬───────────────────────────────────────────┤
│        CLI Executable           │          Web Executable                  │
│    (yt-transcriptions-gui-cli)  │     (yt-transcriptions-gui-web)         │
│                                 │                                           │
│ • Console Application           │ • Windows Native Application           │
│ • Argument Parsing (argparse)   │ • Browser Auto-launch                   │
│ • Command Line Output          │ • Permanent Download Directory         │
│ • User-specified Output        │ • FastAPI Web Framework                 │
│ • Exit Code Support            │ • HTML Template Rendering               │
│ • Error Display to stderr      │ • File Download Management              │
│ • Workflow Orchestration       │ • Form Processing                       │
│ • Cross-platform CLI           │ • Windows-specific optimizations        │
└─────────────────────────────────┴───────────────────────────────────────────┘
```

### Executable Architecture Comparison

| Aspect | CLI Executable | Web Executable |
|--------|----------------|----------------|
| **Entry Point** | `src/cli_main.py:main()` | `src/web_main.py:main()` |
| **Target Users** | Developers, Power Users | End Users, Non-technical |
| **Interface Type** | Console Application | Windows GUI Application |
| **Distribution** | Self-contained EXE | Self-contained EXE |
| **Dependencies** | Core modules only | Core + Web Framework |
| **Output Location** | User-specified | `~/yt-transcriptions/` |
| **File Size** | ~15-20 MB | ~25-30 MB |
| **PyInstaller Type** | `--console` | `--windowed` |
| **Browser Integration** | None | Auto-launch to localhost:8000 |
| **Error Handling** | Console output + Exit codes | HTML error pages |
| **Configuration** | Command-line arguments | Web form interface |
| **Use Cases** | Automation, Scripting, CI/CD | User-friendly access, Quick extraction |

### Executable Entry Points

#### CLI Executable (`yt-transcriptions-gui-cli.exe`)

**File**: `src/cli_main.py`

```python
def main(args=None):
    """Main CLI function for yt-transcriptions-gui-cli."""
    parsed_args = parse_arguments(args)

    # Validate URL
    if not validate_youtube_url(parsed_args.url):
        print(f"Error: Invalid YouTube URL: {parsed_args.url}", file=sys.stderr)
        sys.exit(1)

    # Extract, format, save transcript
    # ...

    print(f"Transcript saved to: {filepath}")
    sys.exit(0)  # Success
```

**Key Features**:
- Argument parsing with `argparse`
- Exit code support for automation
- Error output to stderr
- User-specified output directories

#### Web Executable (`yt-transcriptions-gui-web.exe`)

**File**: `src/web_main.py`

```python
def main():
    """Main entry point for yt-transcriptions-gui-web."""
    # Ensure download directory exists
    success, download_info = ensure_download_directory()

    # Create modified FastAPI app
    app_instance = create_modified_app()

    # Open browser automatically
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()

    # Run server
    uvicorn.run(app_instance, host="127.0.0.1", port=8000)
```

**Key Features**:
- Automatic browser launch
- Permanent download directory (`~/yt-transcriptions/`)
- Windows-specific optimizations
- Embedded web resources (templates, static files)

### Module Dependencies

```
┌─────────────────┐
│     CLI         │
│   Interface     │
└─────────┬───────┘
          │
          ├───► transcriptor.py
          │        ├── youtube-transcript-api (external)
          │        └── utils.py
          │
          ├───► file_handler.py
          │        └── utils.py
          │
          └───► utils.py

┌─────────────────┐
│     Web         │
│   Interface     │
└─────────┬───────┘
          │
          ├───► transcriptor.py (shared)
          │        ├── youtube-transcript-api (external)
          │        └── utils.py (shared)
          │
          ├───► file_handler.py (shared)
          │        └── utils.py (shared)
          │
          └───► FastAPI/Jinja2/uvicorn (web dependencies)
```

## Component Design

### 1. main.py - CLI Interface

**Responsibilities:**
- Command-line argument parsing
- User interface and feedback
- Error handling and user messaging
- Orchestrating the overall workflow

**Key Features:**
- Uses `argparse` for professional CLI experience
- Provides helpful error messages and usage examples
- Implements comprehensive exception handling

**Design Decisions:**
- Separation of argument parsing logic for testability
- Clear separation between CLI and business logic
- Consistent error handling patterns

### 2. transcriptor.py - Core Logic

**Responsibilities:**
- YouTube video URL validation and processing
- Transcript extraction from YouTube API
- Video metadata retrieval
- Error handling for API failures

**Key Features:**
- Robust URL parsing for various YouTube URL formats
- Graceful handling of missing transcripts
- Support for language preference
- Custom exception types for better error handling

**Design Decisions:**
- Encapsulation of YouTube API details
- Flexible language handling with fallbacks
- Clear separation between URL processing and API calls

### 3. file_handler.py - File Operations

**Responsibilities:**
- Transcript formatting (TXT, SRT, VTT)
- File naming and sanitization
- File system operations
- Conflict resolution for duplicate filenames

**Key Features:**
- Multiple output format support
- Automatic filename sanitization
- Conflict resolution with numeric suffixes
- Encoding-aware file writing

**Design Decisions:**
- Format-specific functions for clarity
- Flexible output path handling
- Unicode support for international content

### 4. utils.py - Utilities

**Responsibilities:**
- URL validation
- Text sanitization
- Common utility functions

**Key Features:**
- Regex-based URL validation
- Cross-platform filename sanitization
- Length limiting for filename compatibility

### 5. web_app.py - Web Interface

**Responsibilities:**
- FastAPI web application framework
- HTTP request/response handling
- HTML template rendering with Jinja2
- Form processing and validation
- File download management
- Temporary file handling and cleanup

**Key Features:**
- Modern web framework with automatic API documentation
- Responsive HTML interface with Pico.css styling
- Italian language interface for accessibility
- Real-time transcript preview and download
- Secure file handling with path validation
- Automatic cleanup of temporary resources
- Comprehensive error handling with user-friendly messages

**Web Components:**
- **FastAPI Application**: Modern async web framework
- **Jinja2 Templates**: Dynamic HTML rendering
- **Static Files**: CSS, JavaScript, and asset serving
- **Form Processing**: HTTP form data handling
- **File Downloads**: Secure temporary file management
- **Error Handling**: User-friendly error pages

**Template System:**
```
src/templates/
├── base.html          # Base layout and styling
├── index.html         # Homepage with extraction form
└── result.html        # Results display and download
```

**Endpoints:**
- `GET /`: Homepage with form interface
- `POST /extract`: Process transcript extraction
- `GET /download/{filename}`: File download endpoint
- `GET /health`: Health check for monitoring

**Design Decisions:**
- FastAPI for modern async web capabilities
- Jinja2 for secure template rendering
- Pico.css for minimal, responsive design
- Italian interface for enhanced accessibility
- Shared core logic for consistency

## Data Flow

### Dual-Interface Data Flow

```
                    ┌─────────────────────────────────┐
                    │        User Input               │
                    └─────────────┬───────────────────┘
                                  │
                 ┌────────────────┼────────────────┐
                 │                                │
    ┌────────────▼─────────┐              ┌───────▼───────┐
    │   CLI Interface      │              │ Web Interface │
    │   (main.py)          │              │ (web_app.py)  │
    └────────────┬─────────┘              └───────┬───────┘
                 │                                │
    ┌────────────▼─────────┐              ┌───────▼───────┐
    │   Argument Parsing   │              │ Form Parsing  │
    │   (argparse)         │              │ (FastAPI)     │
    └────────────┬─────────┘              └───────┬───────┘
                 │                                │
                 └────────────┬─────────────────────┘
                              │
                ┌─────────────▼──────────────┐
                │      Shared Core Logic     │
                │   (transcriptor.py)        │
                └─────────────┬──────────────┘
                              │
                ┌─────────────▼──────────────┐
                │     URL Validation         │
                │     (utils.py)             │
                └─────────────┬──────────────┘
                              │
                ┌─────────────▼──────────────┐
                │   YouTube API Integration  │
                │ (youtube-transcript-api)   │
                └─────────────┬──────────────┘
                              │
                ┌─────────────▼──────────────┐
                │   Transcript Processing    │
                │   (transcriptor.py)        │
                └─────────────┬──────────────┘
                              │
                ┌─────────────▼──────────────┐
                │   File Format Conversion   │
                │  (file_handler.py)         │
                └─────────────┬──────────────┘
                              │
                 ┌────────────┼────────────────┐
                 │                            │
    ┌────────────▼─────────┐      ┌───────────▼──────────┐
    │    CLI Output        │      │   Web Response       │
    │   (stdout/file)      │      │  (HTML + Download)   │
    └──────────────────────┘      └──────────────────────┘
```

### CLI Interface Flow

```
1. CLI Input
   ├── YouTube URL (required)
   ├── Format option (--format)
   ├── Language option (--language)
   └── Output directory (--output)

2. Argument Processing
   ├── Parse command line arguments
   ├── Validate required parameters
   └── Set default values

3. Core Processing (shared)
   ├── URL validation
   ├── YouTube API interaction
   ├── Transcript extraction
   ├── Language handling
   └── Metadata retrieval

4. File Processing
   ├── Format conversion (TXT/SRT/VTT)
   ├── Filename sanitization
   ├── File conflict resolution
   └── File system operations

5. User Feedback
   ├── Success confirmation
   ├── File path display
   ├── Error messages
   └── Exit codes
```

### Web Interface Flow

```
1. HTTP Request
   ├── GET / (homepage)
   ├── POST /extract (processing)
   └── GET /download/{file} (download)

2. Form Processing
   ├── Parse form data
   ├── Validate URL format
   ├── Extract parameters
   └── Error checking

3. Core Processing (shared)
   ├── URL validation
   ├── YouTube API interaction
   ├── Transcript extraction
   ├── Language handling
   └── Metadata retrieval

4. Web Processing
   ├── Format conversion (TXT/SRT/VTT)
   ├── Temporary file creation
   ├── Download link generation
   └── Template context preparation

5. HTTP Response
   ├── HTML template rendering
   ├── Error page display
   ├── File download headers
   └── JavaScript interaction

6. Cleanup
   ├── Temporary file removal
   └── Resource cleanup
```

### Error Handling Flow

```
                  ┌─────────────────┐
                  │   Request Start │
                  └────────┬────────┘
                           │
            ┌──────────────┼──────────────┐
            │              │              │
    ┌───────▼──────┐ ┌──────▼─────┐ ┌──────▼──────┐
    │ CLI Input    │ │ Web Input  │ │ Health Check│
    └───────┬──────┘ └──────┬─────┘ └─────────────┘
            │              │
            └──────┬───────┘
                   │
        ┌──────────▼──────────┐
        │   URL Validation    │
        └──────────┬──────────┘
                   │
        ┌──────────▼──────────┐
        │   API Integration   │
        └──────────┬──────────┘
                   │
    ┌──────────────┼──────────────┐
    │              │              │
┌───▼─────┐  ┌─────▼──────┐  ┌────▼──────┐
│ Success │  │ No Transcript│ │ Invalid URL │
└───┬─────┘  └─────┬──────┘  └────┬──────┘
    │              │              │
    │         ┌────▼────┐    ┌────▼─────┐
    │         │Display  │    │Error     │
    │         │Message  │    │Message   │
    │         └─────┬───┘    └─────┬────┘
    │               │              │
    │               └──────┬───────┘
    │                      │
    │        ┌─────────────▼─────────────┐
    │        │   Format Conversion       │
    │        └─────────────┬─────────────┘
    │                      │
    │        ┌─────────────▼─────────────┐
    │        │     File Processing       │
    │        └─────────────┬─────────────┘
    │                      │
    │        ┌─────────────▼─────────────┐
    │        │   Response Generation     │
    │        └─────────────┬─────────────┘
    │                      │
    │          ┌───────────▼───────────┐
    │          │   User Feedback       │
    │          └───────────────────────┘
    └──────────┘

Error Types:
├── InvalidVideoURLError → User-friendly validation message
├── NoTranscriptAvailableError → Guidance for users
└── Generic Exception → Error recovery and logging
```

## Design Patterns

### 1. Strategy Pattern

Applied in transcript formatting:

```python
def format_transcript(transcript_data, format_type: str) -> str:
    if format_type.lower() == "txt":
        return _format_txt(transcript_data)
    elif format_type.lower() == "srt":
        return _format_srt(transcript_data)
    elif format_type.lower() == "vtt":
        return _format_vtt(transcript_data)
    else:
        raise ValueError(f"Unsupported format: {format_type}")
```

### 2. Factory Pattern

Potential for future extension with different transcript sources:

```python
class TranscriptFactory:
    @staticmethod
    def create_transcriptor(source: str):
        if source == "youtube":
            return YouTubeTranscriptor()
        # Future: Add other sources
```

### 3. Template Method Pattern

Applied in the main workflow:

```python
def main(args=None):
    parsed_args = parse_arguments(args)
    validate_url(parsed_args.url)
    transcript_data = extract_transcript(parsed_args.url, parsed_args.language)
    video_title = get_video_title(parsed_args.url)
    formatted_content = format_transcript(transcript_data, parsed_args.format)
    save_transcript(formatted_content, video_title, parsed_args.format, parsed_args.output)
    display_results()
```

## Technology Stack

### Core Dependencies

#### Runtime (Shared)
- **Python 3.13+**: Modern Python with latest language features
- **youtube-transcript-api**: External library for YouTube transcript extraction
- **uv**: Fast Python package manager for dependency management

#### Web Interface Dependencies
- **fastapi>=0.121.2**: Modern, fast web framework for building APIs with Python 3.13+
- **jinja2>=3.1.6**: Modern and designer-friendly templating language for Python
- **python-multipart>=0.0.20**: Streaming multipart parser for Python
- **uvicorn>=0.38.0**: ASGI server implementation for FastAPI applications
- **httpx>=0.28.1**: Async HTTP client for Python (development and testing)

### Development Dependencies

- **pytest>=9.0.1**: Testing framework with powerful features and async support
- **coverage>=7.12.0**: Code coverage measurement and reporting
- **pytest-mock>=3.15.1**: Mocking library for pytest
- **hatchling**: Build system for package distribution

### Standard Libraries Used

#### Core Libraries
- **argparse**: Command-line argument parsing (CLI interface)
- **pathlib**: Modern file system operations with object-oriented interface
- **re**: Regular expressions for URL validation and text processing
- **sys**: System-level operations (exit codes, stderr)
- **tempfile**: Temporary file creation and management
- **shutil**: High-level file operations and directory management

#### Web Libraries
- **asyncio**: Asynchronous I/O operations for FastAPI
- **contextlib**: Context management utilities for resource cleanup
- **typing**: Type hints and annotations for better code documentation

### External Services and Frameworks

#### CSS Framework
- **Pico.css**: Minimalist CSS framework for clean, responsive design
  - CDN-based integration for rapid development
  - Responsive design with mobile-first approach
  - Minimal footprint and browser compatibility

#### Template Engine
- **Jinja2**: Powerful templating engine with:
  - Template inheritance and inclusion
  - Secure template rendering (auto-escaping)
  - Template compilation and caching
  - Extensible filter system

#### Web Server
- **Uvicorn**: High-performance ASGI server with:
  - WebSocket support
  - HTTP/2 capabilities
  - Process management
  - Graceful shutdown handling

### Technology Integration

```
┌─────────────────────────────────────────────────────────────────┐
│                    Technology Stack Integration                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │   Python 3.13   │  │    FastAPI      │  │     Jinja2      │  │
│  │   Runtime       │  │   Framework     │  │   Templates     │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
│           │                     │                     │         │
│           └─────────────────────┼─────────────────────┘         │
│                                 │                               │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              Core Application Logic                      │    │
│  │  ┌─────────────────┐  ┌─────────────────┐               │    │
│  │  │   transcriptor  │  │   file_handler  │               │    │
│  │  │     Module      │  │     Module      │               │    │
│  │  └─────────────────┘  └─────────────────┘               │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                 │                               │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              External Dependencies                       │    │
│  │  ┌─────────────────┐  ┌─────────────────┐               │    │
│  │  │youtube-transcript│  │     Pico.css    │               │    │
│  │  │     -api        │  │   Framework     │               │    │
│  │  └─────────────────┘  └─────────────────┘               │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │               Development & Testing                     │    │
│  │  ┌─────────────────┐  ┌─────────────────┐               │    │
│  │  │    pytest      │  │    coverage     │               │    │
│  │  │   Framework    │  │     Tool        │               │    │
│  │  └─────────────────┘  └─────────────────┘               │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

### Platform Compatibility

#### Supported Platforms
- **Development**: Windows, macOS, Linux
- **Deployment**: Docker containers, cloud platforms, bare metal
- **Web Browsers**: Chrome, Firefox, Safari, Edge (modern versions)

#### Python Environment
- **Minimum Version**: Python 3.13
- **Recommended**: Python 3.13+ with latest security patches
- **Package Manager**: uv (recommended) or pip with virtualenv

### Web Technology Choices

#### FastAPI Selection Rationale
- **Performance**: High-performance async framework
- **Type Hints**: Native Python type hinting support
- **Automatic Documentation**: OpenAPI/Swagger generation
- **Validation**: Pydantic integration for request/response validation
- **Modern Python**: Supports latest Python features

#### Jinja2 Selection Rationale
- **Security**: Automatic HTML escaping
- **Flexibility**: Powerful template inheritance
- **Performance**: Compiled templates
- **Ecosystem**: Mature and well-maintained
- **Integration**: Excellent FastAPI integration

#### Pico.css Selection Rationale
- **Minimalism**: Small footprint, essential styling only
- **Accessibility**: WCAG compliant components
- **Responsiveness**: Mobile-first design approach
- **Browser Support**: Excellent cross-browser compatibility
- **Customization**: Easy to customize and extend

## Security Considerations

### Input Validation

- URL validation prevents malformed inputs
- Filename sanitization prevents path traversal attacks
- Language code validation ensures safe API parameters

### Error Information Exposure

- Generic error messages for internal failures
- Detailed logging for debugging (without exposing sensitive data)
- Safe handling of API responses

### File System Safety

- Automatic directory creation with proper permissions
- Filename sanitization prevents invalid characters
- Conflict resolution prevents accidental overwrites

## Performance Considerations

### Memory Efficiency

- Streaming approach for large transcripts
- Minimal memory footprint for API responses
- Efficient string operations for formatting

### Network Optimization

- Single API call per video
- No video downloads (transcript-only approach)
- Efficient error handling to avoid unnecessary retries

### File Operations

- Atomic file writing where possible
- Efficient encoding handling
- Minimal file system operations

## Scalability Considerations

### Current Limitations

- Single-threaded execution
- No batch processing capabilities
- No caching mechanism
- No rate limiting for API calls

### Potential Enhancements

1. **Batch Processing**: Process multiple URLs in sequence or parallel
2. **Caching**: Cache transcripts to avoid repeated API calls
3. **Rate Limiting**: Respect YouTube API rate limits
4. **Async Operations**: Use async/await for concurrent operations
5. **Database Storage**: Store transcripts in database for search and retrieval

### Extensibility Points

1. **New Output Formats**: Easy to add new formatting functions
2. **Additional Video Sources**: Factory pattern allows new source integrations
3. **Enhanced Metadata**: Extend video information retrieval
4. **Plugin System**: Modular design allows plugin architecture

## Testing Architecture

### Test Categories

1. **Unit Tests**: Individual function testing with comprehensive mocking
2. **Integration Tests**: End-to-end workflow testing
3. **CLI Tests**: Command-line interface testing
4. **Error Case Tests**: Comprehensive error condition testing

### Testing Strategies

- **Mocking**: External API dependencies are fully mocked
- **Fixtures**: Reusable test data and setup
- **Parameterized Tests**: Test multiple input combinations
- **Coverage Goals**: Target 95%+ code coverage

### Test Organization

```
tests/
├── unit/
│   ├── test_transcriptor.py
│   ├── test_file_handler.py
│   └── test_utils.py
├── integration/
│   └── test_integration.py
├── test_main.py
└── test_project_setup.py
```

## Future Architecture Considerations

### Potential Extensions

1. **Web Interface**: Flask/FastAPI web service
2. **API Service**: RESTful API for transcript extraction
3. **Database Integration**: Store and search transcripts
4. **Real-time Processing**: WebSocket support for live updates
5. **Machine Learning**: Transcript analysis and enhancement

### Architectural Patterns for Future Growth

- **Microservices**: Separate service for different functionalities
- **Event-Driven**: Asynchronous processing with message queues
- **CQRS**: Separate read/write operations for scalability
- **Caching Layers**: Redis for transcript caching

## Documentation Architecture

### Documentation Types

1. **API Documentation**: Detailed function and class documentation
2. **Architecture Documentation**: System design and decisions
3. **User Documentation**: Installation and usage guides
4. **Developer Documentation**: Contribution guidelines and setup

### Documentation Maintenance

- **Automated Updates**: API documentation generation from code
- **Version Control**: Documentation versioning with releases
- **Review Process**: Documentation review during code reviews
- **Accessibility**: Multiple formats (Markdown, HTML)