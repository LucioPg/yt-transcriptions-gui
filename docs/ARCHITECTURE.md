# Architecture Documentation

This document provides an overview of the YouTube Transcriptor architecture, design decisions, and technical implementation details.

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

YouTube Transcriptor is a lightweight Python CLI tool designed to extract video transcripts directly from YouTube without downloading the actual video content. The tool follows a modular architecture with clear separation of concerns, making it maintainable and extensible.

### Key Design Principles

1. **Simplicity**: Focus on core functionality without unnecessary complexity
2. **Modularity**: Separate concerns into distinct modules
3. **Testability**: Design for comprehensive testing with mocking
4. **Extensibility**: Easy to add new output formats or features
5. **Robustness**: Graceful error handling and validation

## System Architecture

### High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CLI Interface │───▶│   Business Logic │───▶│   File Handler  │
│   (main.py)     │    │ (transcriptor.py)│    │(file_handler.py)│
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Arg Parsing   │    │   YouTube API   │    │   File System   │
│   (argparse)    │    │   Integration   │    │   Operations    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Utilities     │    │   Validation    │    │   Formatting    │
│  (utils.py)     │    │    Logic        │    │    Functions    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Module Dependencies

```
main.py
├── transcriptor.py
│   ├── youtube-transcript-api (external)
│   └── utils.py
├── file_handler.py
│   └── utils.py
└── utils.py
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

## Data Flow

### Transcript Extraction Flow

```
1. CLI Input
   └── YouTube URL + Options

2. URL Validation
   └── Check URL format and extract video ID

3. API Interaction
   └── Request transcript from YouTube

4. Language Handling
   ├── Try specified language (if provided)
   └── Fallback to first available transcript

5. Metadata Retrieval
   └── Extract video title for filename

6. Formatting
   ├── Convert to requested format (TXT/SRT/VTT)
   └── Apply timestamp formatting

7. File Operations
   ├── Sanitize filename
   ├── Handle conflicts
   └── Write to file system

8. User Feedback
   ├── Success confirmation
   └── Error messages
```

### Error Handling Flow

```
API Call
├── Success → Continue processing
├── No Transcript → NoTranscriptAvailableError
├── Invalid URL → InvalidVideoURLError
└── Network/Other → Generic Exception
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

- **Python 3.13+**: Modern Python with latest language features
- **youtube-transcript-api**: External library for YouTube transcript extraction
- **uv**: Fast Python package manager for dependency management

### Development Dependencies

- **pytest**: Testing framework with powerful features
- **coverage**: Code coverage measurement
- **hatchling**: Build system for package distribution

### Standard Libraries Used

- **argparse**: Command-line argument parsing
- **pathlib**: Modern file system operations
- **re**: Regular expressions for URL validation and text processing
- **sys**: System-level operations (exit codes, stderr)

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