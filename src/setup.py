# src/setup.py
"""
Setup script for YouTube Transcriptor installation.
Ensures required directories exist for proper operation.
"""

import sys
import os
from pathlib import Path

def ensure_download_directory():
    """Ensure the download directory exists in user's home."""
    try:
        home = Path.home()
        download_dir = home / "yt-transcriptions"
        download_dir.mkdir(exist_ok=True)

        # Create a README file in the directory to explain its purpose
        readme_file = download_dir / "README.txt"
        if not readme_file.exists():
            readme_content = """# YouTube Transcriptor Download Directory

This directory contains transcripts downloaded by YouTube Transcriptor.

## Files in this directory
- Files are named using the YouTube video title
- Multiple formats are supported: .txt, .srt, .vtt
- Each file contains the complete transcript of the corresponding video

## Managing files
- You can safely delete files you no longer need
- The directory will be automatically recreated if deleted
- Files are downloaded when you use the "Download" button in the web interface

## Questions
If you have questions about YouTube Transcriptor, please refer to the project documentation.
"""
            with open(readme_file, 'w', encoding='utf-8') as f:
                f.write(readme_content)

        print(f"[OK] Download directory ready: {download_dir}")
        return True

    except Exception as e:
        print(f"Warning: Could not create download directory: {e}")
        return False

def verify_installation():
    """Verify installation requirements and setup directories."""
    print("YouTube Transcriptor - Installation Setup")
    print("=" * 40)

    success = True

    # Ensure download directory exists
    if not ensure_download_directory():
        success = False

    if success:
        print("[OK] Installation setup completed successfully!")
        print("You can now use YouTube Transcriptor with all features enabled.")
    else:
        print("[WARNING] Installation setup completed with warnings.")
        print("Some features may not work as expected.")

    return success

if __name__ == "__main__":
    # Run setup when executed directly
    verify_installation()