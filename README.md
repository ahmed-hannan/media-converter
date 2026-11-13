# Media Converter

A lightweight Python library and command-line utility designed for fast, local conversion between common Apple media formats and cross-platform standards:

- **MOV to MP4**: High-compatibility H.264/AAC transcoding via FFmpeg with web-streaming optimization (`+faststart`).
- **HEIC to PNG**: Lossless image decoding with automatic EXIF rotation handling via `pillow-heif` and `Pillow`.

---

## Installation

Ensure you have Python 3.9 or newer installed:

```bash
pip install -r requirements.txt
```

*Note: FFmpeg is automatically discovered from your system PATH, or through the bundled binary provided by `imageio-ffmpeg`.*

---

## Usage

### Command-Line Interface (CLI)

```bash
# Convert a single video
python main.py video path/to/sample.mov -o output.mp4

# Convert a single image
python main.py image path/to/sample.heic -o output.png

# Batch convert a folder containing MOV and HEIC files
python main.py batch path/to/input_folder -o path/to/output_folder
```

### Python API

```python
from media_converter import convert_mov_to_mp4, convert_heic_to_png

# Video conversion
convert_mov_to_mp4("sample.mov", "output.mp4")

# Image conversion
convert_heic_to_png("sample.heic", "output.png")
```

---

## Testing

Run unit tests using `pytest` or Python's standard `unittest` module:

```bash
python -m unittest discover tests
```
