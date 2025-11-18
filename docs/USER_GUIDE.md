# YouTube Transcriptor User Guide

This comprehensive guide helps you get the most out of YouTube Transcriptor, whether you prefer a user-friendly web interface or powerful command-line tools.

## Table of Contents

- [Getting Started](#getting-started)
- [Web Interface (yt-transcriptor-web.exe)](#web-interface-yt-transcriptor-webexe)
- [Command Line Interface (yt-transcriptor-cli.exe)](#command-line-interface-yt-transcriptor-cliee)
- [Output Formats](#output-formats)
- [File Management](#file-management)
- [Troubleshooting](#troubleshooting)
- [Advanced Usage](#advanced-usage)

## Getting Started

### What is YouTube Transcriptor?

YouTube Transcriptor extracts video transcripts directly from YouTube without downloading the video itself. This saves time, bandwidth, and storage space while giving you access to video content in text format.

### Two Ways to Use YouTube Transcriptor

1. **Web Interface** - Easy to use, visual interface for everyday users
2. **Command Line** - Powerful interface for automation and advanced users

Choose the one that best fits your needs!

---

## Web Interface (yt-transcriptor-web.exe)

### Quick Start

1. **Double-click** `yt-transcriptor-web.exe`
2. **Wait** for your browser to open automatically
3. **Paste** a YouTube URL in the box
4. **Click** "Extract Transcript"
5. **Download** your transcript file

### What Happens When You Start

- A small window appears briefly
- Your default web browser opens to http://localhost:8000
- The web interface loads in your browser
- Your transcript files are saved to `~/yt-transcriptions/`

### Using the Web Interface

#### Step 1: Enter YouTube URL
```
Supported formats:
• https://www.youtube.com/watch?v=VIDEO_ID
• https://youtu.be/VIDEO_ID
• https://www.youtube.com/embed/VIDEO_ID
```

#### Step 2: Choose Options
- **Format**:
  - `TXT` - Plain text for reading
  - `SRT` - Subtitle format for video players
  - `VTT` - Web video text tracks format
- **Language**: Leave blank for auto-detection, or specify (en, it, es, etc.)

#### Step 3: Extract and Download
- Click "Extract Transcript"
- Preview the transcript on screen
- Click the download button to save the file

### Web Interface Features

#### 🎨 User-Friendly Design
- Clean, simple interface
- Works on all modern browsers
- Mobile-friendly responsive design

#### 📁 Automatic File Management
- Files automatically saved to your home folder
- Organized in `~/yt-transcriptions/` directory
- Automatic README file with instructions
- No need to choose save locations

#### 🌍 Language Support
- Auto-detect available languages
- Manual language selection
- Support for multiple transcript languages

#### ❌ Helpful Error Messages
- Clear feedback for invalid URLs
- Helpful guidance when transcripts aren't available
- Suggestions for troubleshooting

### Where Files Are Saved

```
Your Home Folder/
└── yt-transcriptions/
    ├── README.txt                           # Information about this folder
    ├── Video_Title_1.txt                    # Plain text transcript
    ├── Video_Title_2.srt                    # SRT subtitle file
    └── Video_Title_3.vtt                    # VTT web subtitle file
```

**How to find your files:**
- Windows: `C:\Users\YourName\yt-transcriptions\`
- Press `Windows Key + R` and type: `%USERPROFILE%\yt-transcriptions`

---

## Command Line Interface (yt-transcriptor-cli.exe)

### Quick Start

1. **Open Command Prompt** or PowerShell
2. **Navigate** to where you saved the executable
3. **Run**: `yt-transcriptor-cli.exe "https://youtu.be/VIDEO_ID"`

### Basic Usage

#### Extract Transcript (Simple)
```bash
yt-transcriptor-cli.exe "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
```
Output: `transcriptions/Video_Title.txt`

#### With Options
```bash
yt-transcriptor-cli.exe "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --format srt --language en
```
Output: `transcriptions/Video_Title.srt`

#### Custom Output Directory
```bash
yt-transcriptor-cli.exe "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --output "C:\My Transcripts"
```

### Command Line Options

| Option | Short | Description | Example |
|--------|-------|-------------|---------|
| `--format` | `-f` | Output format | `--format srt` |
| `--language` | `-l` | Language code | `--language en` |
| `--output` | `-o` | Output directory | `--output "C:\Docs"` |
| `--help` | `-h` | Show help | `--help` |

### Format Options

#### TXT Format (Default)
- Plain text transcript
- Easy to read and edit
- Good for documentation
- Smallest file size

```bash
yt-transcriptor-cli.exe "URL" --format txt
```

#### SRT Format
- Standard subtitle format
- Compatible with video players
- Includes timing information
- Good for video captioning

```bash
yt-transcriptor-cli.exe "URL" --format srt
```

#### VTT Format
- Web video text tracks
- Compatible with web players
- HTML5 video support
- Good for web applications

```bash
yt-transcriptor-cli.exe "URL" --format vtt
```

### Language Options

#### Auto-Detect (Default)
```bash
yt-transcriptor-cli.exe "URL"
```
Automatically uses the first available language.

#### Specify Language
```bash
yt-transcriptor-cli.exe "URL" --language en    # English
yt-transcriptor-cli.exe "URL" --language es    # Spanish
yt-transcriptor-cli.exe "URL" --language it    # Italian
yt-transcriptor-cli.exe "URL" --language fr    # French
```

#### Common Language Codes
- `en` - English
- `es` - Spanish
- `it` - Italian
- `fr` - French
- `de` - German
- `pt` - Portuguese
- `ru` - Russian
- `ja` - Japanese
- `ko` - Korean
- `zh` - Chinese

### Advanced Command Line Usage

#### Batch Processing
Create a batch file to process multiple URLs:

```batch
@echo off
echo Processing multiple videos...

yt-transcriptor-cli.exe "https://www.youtube.com/watch?v=VIDEO1" --format srt
yt-transcriptor-cli.exe "https://www.youtube.com/watch?v=VIDEO2" --format vtt
yt-transcriptor-cli.exe "https://www.youtube.com/watch?v=VIDEO3" --language en

echo All transcripts extracted!
pause
```

#### Scripting Examples

**PowerShell Script:**
```powershell
$urls = @(
    "https://www.youtube.com/watch?v=VIDEO1",
    "https://www.youtube.com/watch?v=VIDEO2",
    "https://www.youtube.com/watch?v=VIDEO3"
)

foreach ($url in $urls) {
    Write-Host "Processing: $url"
    & ".\yt-transcriptor-cli.exe" $url --format txt --output "C:\MyTranscripts"
}
```

**Command in a Loop:**
```bash
for /f %i in (urls.txt) do yt-transcriptor-cli.exe "%i" --format srt
```
(Save URLs in `urls.txt`, one per line)

### Command Line Examples

#### Educational Content
```bash
# Extract educational lecture in SRT format
yt-transcriptor-cli.exe "LECTURE_URL" --format srt --language en --output "C:\Lectures"
```

#### Podcast Transcripts
```bash
# Extract podcast transcript as plain text
yt-transcriptor-cli.exe "PODCAST_URL" --format txt --output "C:\Podcasts"
```

#### Multi-Language Content
```bash
# Extract transcript in different languages
yt-transcriptor-cli.exe "VIDEO_URL" --language es --output "Spanish"
yt-transcriptor-cli.exe "VIDEO_URL" --language fr --output "French"
```

---

## Output Formats

### TXT Format - Plain Text

**Best for:** Reading, documentation, searching

**Example:**
```
Hello world, this is a transcript example.
This is the second line of the transcript.

Speaker: And this is a different person speaking.
This makes it easy to read who said what.
```

**File size:** Smallest
**Compatibility:** Universal
**Editing:** Easy in any text editor

### SRT Format - Subtitles

**Best for:** Video players, subtitle editing, timing

**Example:**
```srt
1
00:00:00,000 --> 00:00:02,500
Hello world, this is a transcript example.

2
00:00:02,500 --> 00:00:05,000
This is the second line of the transcript.

3
00:00:05,000 --> 00:00:08,000
Speaker: And this is a different person speaking.
```

**File size:** Medium
**Compatibility:** VLC, Media Player Classic, YouTube
**Editing:** Specialized subtitle editors

### VTT Format - Web Video

**Best for:** Web video, HTML5 players, online platforms

**Example:**
```vtt
WEBVTT

00:00:00.000 --> 00:00:02.500
Hello world, this is a transcript example.

00:00:02.500 --> 00:00:05.000
This is the second line of the transcript.

00:00:05.000 --> 00:00:08.000
Speaker: And this is a different person speaking.
```

**File size:** Medium
**Compatibility:** Web browsers, YouTube, online players
**Editing:** Text editors with syntax highlighting

---

## File Management

### Web Interface File Organization

The web interface automatically creates and manages your transcript files:

```
~/yt-transcriptions/
├── README.txt                           # Information about this folder
├── Rick_Astley_Never_Gonna_Give_You_Up.txt
├── Python_Tutorial_for_Beginners.srt
├── Cooking_Show_Episode_1.vtt
└── History_Documentary_WWII.txt
```

### CLI File Organization

The CLI saves files where you specify:

```bash
# Default location
yt-transcriptor-cli.exe "URL"
# Saves to: ./transcriptions/Video_Title.txt

# Custom location
yt-transcriptor-cli.exe "URL" --output "C:\My Documents\Transcripts"
# Saves to: C:\My Documents\Transcripts\Video_Title.txt
```

### File Naming

Files are automatically named based on the YouTube video title:

- **Special characters** are replaced with safe alternatives
- **Long titles** are truncated to reasonable lengths
- **Duplicate files** get numbers appended (e.g., `Video_Title_2.txt`)

### File Management Tips

#### Organizing by Topic
```bash
# Create organized folders
mkdir "C:\Transcripts\Education"
mkdir "C:\Transcripts\Entertainment"
mkdir "C:\Transcripts\Technology"

# Save to appropriate folders
yt-transcriptor-cli.exe "EDUCATION_URL" --output "C:\Transcripts\Education"
yt-transcriptor-cli.exe "TECH_URL" --output "C:\Transcripts\Technology"
```

#### Date-based Organization
```bash
# Create dated folders
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "datefolder=%YYYY%-%MM%-%DD%"

mkdir "C:\Transcripts\%datefolder%"
yt-transcriptor-cli.exe "URL" --output "C:\Transcripts\%datefolder%"
```

---

## Troubleshooting

### Common Problems and Solutions

#### "Invalid YouTube URL" Error

**Problem:** The URL doesn't look like a YouTube link.

**Solutions:**
1. **Copy the full URL** from your browser's address bar
2. **Use these formats:**
   - `https://www.youtube.com/watch?v=VIDEO_ID`
   - `https://youtu.be/VIDEO_ID`
   - `https://www.youtube.com/embed/VIDEO_ID`

**Example:**
```
✓ Valid: https://www.youtube.com/watch?v=dQw4w9WgXcQ
✗ Invalid: youtube.com/watch?v=dQw4w9WgXcQ
✗ Invalid: https://youtu.be/dQw4w9WgXcQ&t=30s
```

#### "No transcript available" Error

**Problem:** The video doesn't have captions or transcripts.

**Solutions:**
1. **Check manually**: Go to the video on YouTube, click CC (closed captions)
2. **Try different language**: Some videos only have transcripts in certain languages
3. **Alternative video**: Look for similar videos with transcripts available

#### "Web interface won't open" Error

**Problem:** The browser doesn't open or shows an error.

**Solutions:**
1. **Wait 10-15 seconds** after running the executable
2. **Open manually**: Type `http://localhost:8000` in your browser
3. **Check for conflicts**: Make sure port 8000 isn't being used by another program
4. **Firewall**: Allow the program through Windows Firewall if prompted

#### "File not found" or "Access denied" Errors

**Problem:** Can't save files to specified location.

**Solutions:**
1. **Check permissions**: Make sure you have write access to the folder
2. **Use a different location**: Try saving to your Desktop or Documents folder
3. **Create folder first**: Make sure the output directory exists
4. **Run as administrator**: Right-click and "Run as administrator"

#### Large file taking too long

**Problem:** Very long videos seem to hang.

**Solutions:**
1. **Be patient**: 1-hour videos can take 30-60 seconds
2. **Check network connection**: Slow internet can slow down extraction
3. **Try shorter videos**: Test with a 5-minute video first

### Getting Help

#### What to Include When Asking for Help

1. **YouTube URL** (the one causing problems)
2. **Error message** (exact text)
3. **What you tried** (steps you took)
4. **Your setup** (Windows version, executable used)

#### Where to Get Help
- **GitHub Issues**: Report bugs at the project repository
- **Documentation**: Check this guide and other documentation
- **Community**: Join discussions or forums for the project

---

## Advanced Usage

### Automation with Scripts

#### Daily Transcript Extraction

**Windows Task Scheduler + Batch File:**

1. Create `extract_daily.bat`:
```batch
@echo off
echo Extracting daily transcripts...
yt-transcriptor-cli.exe "https://www.youtube.com/watch?v=DAILY_VIDEO" --format txt --output "C:\Daily Transcripts"
echo Done!
```

2. Set up Windows Task Scheduler to run this batch file daily.

#### YouTube Playlist Processing

**PowerShell script to process entire playlist:**
```powershell
# Note: This requires a separate playlist URL extractor
# This is a conceptual example

$playlistUrls = @(
    "https://www.youtube.com/watch?v=VIDEO1",
    "https://www.youtube.com/watch?v=VIDEO2",
    "https://www.youtube.com/watch?v=VIDEO3"
)

$outputFolder = "C:\Playlist Transcripts"

foreach ($url in $playlistUrls) {
    Write-Host "Processing: $url"
    & ".\yt-transcriptor-cli.exe" $url --format txt --output $outputFolder
    Start-Sleep -Seconds 5  # Wait between requests
}
```

### Integration with Other Tools

#### Combine with Text Analysis
```bash
# Extract transcript
yt-transcriptor-cli.exe "URL" --format txt --output "C:\Analysis"

# Then use with text analysis tools
# For example: word frequency, summarization, etc.
```

#### Create Summary Documents
```bash
# Extract multiple related videos
yt-transcriptor-cli.exe "URL1" --output "C:\Course\Week1"
yt-transcriptor-cli.exe "URL2" --output "C:\Course\Week2"
yt-transcriptor-cli.exe "URL3" --output "C:\Course\Week3"

# Files are organized for easy reference
```

### Tips and Best Practices

#### For Researchers
- **Use SRT format** for timestamp accuracy
- **Extract in original language** for authenticity
- **Organize by project or topic**
- **Keep backup of important transcripts**

#### For Content Creators
- **Extract competitor videos** for research
- **Use transcripts for content planning**
- **Extract your own videos** for SEO optimization
- **Create written content from video transcripts**

#### For Students
- **Extract lecture recordings** for study notes
- **Use TXT format** for easy searching
- **Organize by subject or course**
- **Highlight and annotate transcripts**

#### For Accessibility
- **Extract transcripts** for hearing-impaired users
- **Create written documentation** from video content
- **Translate transcripts** for multi-language support

---

## FAQ

### General Questions

**Q: Do I need to install anything to use the executables?**
A: No! The executables are self-contained and include everything needed.

**Q: Will this work on Mac or Linux?**
A: Currently, the executables are Windows-only. Mac/Linux support is planned.

**Q: How much space do the executables take?**
A: About 15-30 MB for the executables, plus space for your transcript files.

**Q: Can I extract transcripts from private videos?**
A: Only if you have access to the video and it has transcripts available.

### Technical Questions

**Q: What video formats work?**
A: Any YouTube video URL that has closed captions or transcripts enabled.

**Q: Can I extract transcripts from live streams?**
A: Only if the live stream has automated captions enabled and saved.

**Q: Is there a limit to how many transcripts I can extract?**
A: No built-in limit, but be respectful of YouTube's terms of service.

### Legal Questions

**Q: Is it legal to extract YouTube transcripts?**
A: Generally yes for personal use, but check YouTube's Terms of Service.

**Q: Can I use extracted transcripts commercially?**
A: Be careful - transcripts may be copyrighted. Use responsibly.

---

## Keyboard Shortcuts and Tips

### Web Interface
- `Tab`: Navigate between form fields
- `Enter`: Submit the form
- `Ctrl+C`: Copy transcript text
- `Ctrl+S`: Save transcript (in browser)

### Command Line
- `↑`: Previous command
- `Tab`: Auto-complete file paths
- `Ctrl+C`: Cancel extraction
- `→` and `←`: Edit command line

### Productivity Tips
- **Save URLs** in a text file for batch processing
- **Use descriptive folder names** for organization
- **Test with short videos** before processing long ones
- **Backup important transcripts** to cloud storage

---

## Getting Help and Contributing

### Documentation
- **User Guide** (this file): Complete usage instructions
- **API Documentation**: Technical details for developers
- **Architecture Guide**: System design information

### Community
- **GitHub Issues**: Report bugs and request features
- **Discussions**: Ask questions and share tips
- **Wiki**: Community-contributed guides and examples

### Contributing
We welcome contributions! See the CONTRIBUTING.md file for details on:
- Reporting bugs
- Suggesting features
- Submitting pull requests
- Improving documentation

---

**Thank you for using YouTube Transcriptor!**

This tool is designed to make transcript extraction easy and accessible for everyone, whether you're a student, researcher, content creator, or just curious about video content.