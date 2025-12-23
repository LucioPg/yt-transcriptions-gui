# Building Windows Executables

This guide provides comprehensive instructions for building Windows executables for YouTube Transcriptions GUI. The project supports two separate executables targeting different user needs.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Quick Build](#quick-build)
- [Detailed Build Process](#detailed-build-process)
- [Executable Specifications](#executable-specifications)
- [Testing Executables](#testing-executables)
- [Distribution](#distribution)
- [Troubleshooting](#troubleshooting)

## Overview

YouTube Transcriptions GUI provides two Windows executables:

### yt-transcriptions-gui-cli.exe
- **Target Audience**: Developers, power users, automation scripts
- **Interface**: Command-line console
- **Usage**: `yt-transcriptions-gui-cli.exe <URL> [options]`
- **Output**: User-specified directory
- **Size**: ~15-20 MB

### yt-transcriptions-gui-web.exe
- **Target Audience**: Everyday users, non-technical users
- **Interface**: Web browser (automatically launched)
- **Usage**: Double-click executable
- **Output**: `~/yt-transcriptions/` (automatic)
- **Size**: ~25-30 MB

## Prerequisites

### System Requirements
- **Operating System**: Windows 10 or later
- **Python**: 3.13+ (for building only)
- **Package Manager**: uv (recommended)
- **Build Tools**: PyInstaller (automatically installed)

### Development Environment Setup

```bash
# Clone the repository
git clone https://github.com/LucioPG/yt-transcriptions-gui.git
cd yt-transcriptions-gui

# Set up Python environment
uv sync

# Install packaging dependencies
uv sync --extra packaging

# Verify setup
uv run python -m pytest tests/
```

## Quick Build

### Using Makefile (Recommended)

```bash
# Build both executables
make build-all-exe

# Build individual executables
make build-cli-exe    # CLI executable only
make build-web-exe    # Web executable only

# Test built executables
make test-exe
```

### Output Location
After building, executables will be in the `dist/` directory:
- `dist/yt-transcriptions-gui-cli.exe`
- `dist/yt-transcriptions-gui-web.exe`

## Detailed Build Process

### 1. CLI Executable Build

#### Using PyInstaller Directly
```bash
# Navigate to project root
cd yt-transcriptions-gui

# Build CLI executable
uv run pyinstaller --onefile --console \
  --name "yt-transcriptions-gui-cli" \
  --hidden-import=transcriptor \
  --hidden-import=file_handler \
  --hidden-import=utils \
  src/cli_main.py
```

#### Using Spec File
```bash
# Build using the existing spec file
uv run pyinstaller yt-transcriptions-gui-cli.spec
```

### 2. Web Executable Build

#### Using PyInstaller Directly
```bash
# Build web executable with embedded resources
uv run pyinstaller --onefile --windowed \
  --name "yt-transcriptions-gui-web" \
  --add-data "src/templates;templates" \
  --add-data "src/static;static" \
  --hidden-import=transcriptor \
  --hidden-import=file_handler \
  --hidden-import=utils \
  --hidden-import=fastapi \
  --hidden-import=jinja2 \
  --hidden-import=uvicorn \
  src/web_main.py
```

#### Create Web Executable Spec File
Create `yt-transcriptions-gui-web.spec`:
```python
# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['src\\web_main.py'],
    pathex=['src'],
    binaries=[],
    datas=[
        ('src\\templates', 'templates'),
        ('src\\static', 'static'),
    ],
    hiddenimports=[
        'transcriptor',
        'file_handler',
        'utils',
        'fastapi',
        'jinja2',
        'uvicorn',
        'python_multipart'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='yt-transcriptions-gui-web',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Windowed application
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
```

## Executable Specifications

### CLI Executable Configuration
- **Entry Point**: `src/cli_main.py:main`
- **Type**: Console application
- **Dependencies**: Core modules + youtube-transcript-api
- **Command Line Support**: Full argument parsing with argparse
- **Error Handling**: Console output with proper exit codes

### Web Executable Configuration
- **Entry Point**: `src/web_main.py:main`
- **Type**: Windowed application (no console)
- **Embedded Resources**: Templates and static files
- **Auto-launch**: Opens browser to http://localhost:8000
- **Download Directory**: Creates `~/yt-transcriptions/`
- **Server**: Built-in Uvicorn server

### Key Differences

| Feature | CLI Executable | Web Executable |
|---------|----------------|----------------|
| **Interface** | Console | Browser |
| **Auto-launch** | No | Yes (browser) |
| **Output Location** | User-specified | `~/yt-transcriptions/` |
| **Dependencies** | Minimal only | Web framework |
| **File Size** | ~15-20 MB | ~25-30 MB |
| **Use Case** | Automation, scripting | User-friendly access |

## Testing Executables

### CLI Executable Testing

```bash
# Test help functionality
dist/yt-transcriptions-gui-cli.exe --help

# Test basic transcript extraction
dist/yt-transcriptions-gui-cli.exe "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Test with options
dist/yt-transcriptions-gui-cli.exe "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  --format srt \
  --language en \
  --output ./test_output

# Test error handling
dist/yt-transcriptions-gui-cli.exe "invalid-url"
```

### Web Executable Testing

```bash
# Run the web executable
dist/yt-transcriptions-gui-web.exe

# Manual testing checklist:
# 1. Verify browser opens automatically
# 2. Confirm web interface loads correctly
# 3. Test transcript extraction through web form
# 4. Verify download functionality
# 5. Check files appear in ~/yt-transcriptions/
# 6. Test error handling (invalid URLs, no transcripts)
```

### Automated Testing with Makefile

```bash
# Test both executables
make test-exe

# Test specific executable
make test-cli-exe
```

## Distribution

### File Structure for Release

Create a release package with the following structure:
```
yt-transcriptions-gui-v1.0.0/
├── README.txt                       # Installation and usage instructions
├── LICENSE.txt                      # License information
├── yt-transcriptions-gui-cli.exe   # CLI executable
├── yt-transcriptions-gui-web.exe   # Web executable
└── examples/                        # Example usage scripts
    ├── batch_extract.bat            # Batch processing example
    └── api_usage.txt                # API examples
```

### Creating Release Package

```bash
# Create release directory
mkdir yt-transcriptions-gui-v1.0.0
cd yt-transcriptions-gui-v1.0.0

# Copy executables
cp ../dist/yt-transcriptions-gui-cli.exe .
cp ../dist/yt-transcriptions-gui-web.exe .

# Create README for release
echo "YouTube Transcriptions GUI v1.0.0

This package contains two Windows executables for extracting YouTube transcripts.

QUICK START:
1. Run yt-transcriptions-gui-web.exe for a user-friendly web interface
2. Run yt-transcriptions-gui-cli.exe --help for command-line options

For more information, visit: https://github.com/LucioPG/yt-transcriptions-gui" > README.txt

# Copy license
cp ../LICENSE.txt .

# Create examples
mkdir examples
echo "@echo off
echo Extracting transcript from example video...
yt-transcriptions-gui-cli.exe \"https://www.youtube.com/watch?v=dQw4w9WgXcQ\" --format txt --output ./transcripts
pause" > examples/batch_extract.bat

# Package for distribution
cd ..
zip -r yt-transcriptions-gui-v1.0.0.zip yt-transcriptions-gui-v1.0.0/
```

### GitHub Release

1. Create a new release on GitHub
2. Upload both executables as release assets
3. Include the zip package as well
4. Provide clear installation instructions in the release notes

## Troubleshooting

### Common Build Issues

#### 1. Missing Data Files
**Error**: Templates or static files not found in web executable

**Solution**: Ensure proper data file inclusion:
```bash
--add-data "src/templates;templates" \
--add-data "src/static;static"
```

#### 2. Import Errors
**Error**: ModuleNotFoundError for transcriptor, file_handler, or utils

**Solution**: Add explicit hidden imports:
```bash
--hidden-import=transcriptor \
--hidden-import=file_handler \
--hidden-import=utils
```

#### 3. Permission Issues
**Error**: Access denied during build or execution

**Solution**:
- Run build process as administrator
- Disable User Account Control temporarily
- Check antivirus software isn't blocking executables

#### 4. Large File Sizes
**Error**: Executables too large (>50MB)

**Solution**:
- Use UPX compression (enabled by default)
- Exclude unnecessary modules with `--exclude-module`
- Optimize imports in source code

#### 5. Web Interface Not Loading
**Error**: Browser opens but web interface doesn't load

**Solution**:
- Check if templates are properly embedded
- Verify port 8000 is not in use
- Check Windows firewall settings

### Debug Builds

#### Create Debug Version
```bash
# CLI debug build
uv run pyinstaller --onefile --console --debug all \
  --name "yt-transcriptor-cli-debug" \
  src/cli_main.py

# Web debug build
uv run pyinstaller --onefile --windowed --debug all \
  --name "yt-transcriptor-web-debug" \
  --add-data "src/templates;templates" \
  --add-data "src/static;static" \
  src/web_main.py
```

#### Analyze Build Process
```bash
# Verbose build output
uv run pyinstaller --onefile --log-level DEBUG \
  src/cli_main.py

# Check imports analysis
uv run pyinstaller --onefile --debug imports \
  src/cli_main.py
```

### Platform-Specific Issues

#### Windows Defender Warnings
- Solution: Sign executables with code signing certificate
- Alternative: Add exclusions in Windows Defender

#### Windows 7 Compatibility
- Python 3.13+ may not be compatible with Windows 7
- Consider building with Python 3.8-3.9 for legacy support

#### Antivirus False Positives
- Submit executables to antivirus vendors for whitelisting
- Use code signing to establish trust

## Advanced Configuration

### Custom Icon

```bash
# Add icon to executables
uv run pyinstaller --onefile --console \
  --icon=assets/icon.ico \
  --name "yt-transcriptor-cli" \
  src/cli_main.py

uv run pyinstaller --onefile --windowed \
  --icon=assets/icon.ico \
  --name "yt-transcriptor-web" \
  src/web_main.py
```

### Version Information

```bash
# Add version metadata
uv run pyinstaller --onefile --console \
  --version-file=version_info.txt \
  --name "yt-transcriptor-cli" \
  src/cli_main.py
```

### Optimization

```bash
# Build with optimizations
uv run pyinstaller --onefile --console \
  --optimize 2 \
  --strip \
  --upx-dir=/path/to/upx \
  src/cli_main.py
```

This build guide provides everything needed to create, test, and distribute Windows executables for YouTube Transcriptor. The dual-executable approach ensures optimal user experience for both technical and non-technical users.