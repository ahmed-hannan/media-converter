# Media Converter

A high-performance command-line tool and Python library for converting Apple media formats to cross-platform web standards:
- **MOV to MP4**: Transcodes Apple QuickTime (`.mov`) files to H.264/AAC (`.mp4`) via FFmpeg with web-friendly streaming optimizations (`+faststart`).
- **HEIC to PNG**: Converts Apple High Efficiency Image Container (`.heic`, `.heif`) files to standard PNG with automatic EXIF orientation correction.

---

## Features

- **Automated Dependency Discovery**: Finds system `ffmpeg` on `PATH` or seamlessly falls back to bundled `imageio-ffmpeg` binaries.
- **Batch Processing**: Convert individual files or entire folders (including recursive directory traversals).
- **Quality & Performance Tuning**: Configurable Constant Rate Factor (`--crf`), encoding presets (`--preset`), and lossless compression levels.
- **Orientation Awareness**: Automatically rotates HEIC images according to EXIF metadata so orientations remain correct.
- **Dual Interface**: Full-featured CLI commands and importable Python API.

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/ahmed-hannan/media-converter.git
cd media-converter
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

To install the CLI tool locally in editable mode:

```bash
pip install -e .
```

---

## CLI Usage

You can use `python main.py` or the installed `media-convert` command.

### 1. Convert MOV to MP4

```bash
# Convert with default settings (H.264, CRF 23, medium preset)
python main.py video path/to/input.mov

# Specify custom output destination and quality factor
python main.py video input.mov -o output.mp4 --crf 18 --preset slow
```

### 2. Convert HEIC to PNG

```bash
# Convert single image
python main.py image photo.heic

# Convert with custom output file path
python main.py image photo.heic -o converted.png
```

### 3. Batch Convert a Directory

```bash
# Convert all MOV and HEIC files in a directory
python main.py batch ./raw_media -o ./converted_media

# Convert only images recursively
python main.py batch ./photos -o ./png_photos --type image --recursive

# Convert only videos
python main.py batch ./videos -o ./mp4_videos --type video
```

---

## Python API Usage

```python
from media_converter import (
    convert_mov_to_mp4,
    batch_convert_videos,
    convert_heic_to_png,
    batch_convert_images,
)

# Convert single video
mp4_path = convert_mov_to_mp4("sample.mov", "sample.mp4", crf=20)

# Convert single image
png_path = convert_heic_to_png("sample.heic", "sample.png")

# Batch convert images in a directory
converted_images = batch_convert_images(
    input_dir="./raw_photos",
    output_dir="./processed_photos",
    recursive=True
)

# Batch convert videos in a directory
converted_videos = batch_convert_videos(
    input_dir="./raw_videos",
    output_dir="./processed_videos",
    crf=22
)
```

---

## Project Structure

```text
media-converter/
├── src/
│   └── media_converter/
│       ├── __init__.py       # Package exports
│       ├── cli.py            # Command-line interface definition
│       ├── ffmpeg_utils.py   # FFmpeg binary resolution and execution
│       ├── image.py          # HEIC to PNG conversion functions
│       └── video.py          # MOV to MP4 conversion functions
├── tests/
│   ├── __init__.py
│   ├── test_cli.py           # CLI invocation tests
│   ├── test_image.py         # Image conversion tests
│   └── test_video.py         # Video conversion tests
├── main.py                   # Direct CLI entrypoint
├── pyproject.toml            # Build metadata and package configuration
├── requirements.txt          # Python dependencies
└── README.md                 # Documentation
```

---

## Running Tests

Execute the unit test suite with:

```bash
python -m unittest discover tests
```
