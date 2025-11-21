#!/usr/bin/env python3
"""
Script to convert SVG icon to multiple PNG sizes for Tauri v2 application.
Maintains exact proportions from the original SVG design.
"""

import os
import io
from PIL import Image
import cairosvg

def generate_icons():
    """Generate icons from SVG in various sizes for Tauri v2"""
    sizes = [32, 48, 64, 256]
    output_dir = "src-tauri/icons"
    svg_file = "src-tauri/icons/icon.svg"

    # Ensure the icons directory exists
    os.makedirs(output_dir, exist_ok=True)

    print("Generating icons from SVG...")

    # Convert SVG to PNG for each size
    for size in sizes:
        png_filename = f"{size}x{size}.png"
        png_filepath = os.path.join(output_dir, png_filename)

        print(f"Creating {png_filename}...")

        # Convert SVG to PNG maintaining exact proportions
        cairosvg.svg2png(
            url=svg_file,
            write_to=png_filepath,
            output_width=size,
            output_height=size
        )

    # Create ICO file for Windows using 32x32, 48x48, and 256x256 sizes
    print("Creating favicon.ico...")
    ico_sizes = [32, 48, 256]
    ico_images = []

    for size in ico_sizes:
        # Convert SVG to PNG in memory
        png_data = cairosvg.svg2png(
            url=svg_file,
            output_width=size,
            output_height=size
        )

        # Load the image from memory and add to ICO list
        img = Image.open(io.BytesIO(png_data))
        ico_images.append(img)

    # Save ICO file
    ico_filepath = os.path.join(output_dir, "favicon.ico")
    ico_images[0].save(ico_filepath, format="ICO", sizes=[(size, size) for size in ico_sizes])

    print("All icons generated successfully!")
    print(f"Icons saved in: {output_dir}")
    print(f"Generated sizes: {sizes}")
    print(f"ICO file contains sizes: {ico_sizes}")

if __name__ == "__main__":
    generate_icons()