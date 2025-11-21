#!/usr/bin/env python3
"""
Convert PNG files to ICO format for Tauri application
"""

from PIL import Image
import os

def convert_png_to_ico():
    """Convert all PNG files to ICO format"""
    sizes = [32, 48, 64, 128, 256]
    icons_dir = "src-tauri/icons"

    print("Converting PNG files to ICO...")

    # Change to icons directory
    os.chdir(icons_dir)

    for size in sizes:
        png_file = f"{size}x{size}.png"
        ico_file = f"{size}x{size}.ico"

        if os.path.exists(png_file):
            print(f"Converting {png_file} to {ico_file}")

            # Open PNG and convert to ICO
            img = Image.open(png_file)
            img.save(ico_file, format='ICO', sizes=[(size, size)])

            print(f"Created {ico_file}")
        else:
            print(f"File {png_file} not found")

if __name__ == "__main__":
    convert_png_to_ico()