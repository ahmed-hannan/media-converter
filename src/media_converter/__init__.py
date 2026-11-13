"""Media Converter - High-performance local media conversion library."""

from .video import convert_mov_to_mp4, batch_convert_videos
from .image import convert_heic_to_png, batch_convert_images
from .ffmpeg_utils import get_ffmpeg_path, run_ffmpeg
from .cli import main

__all__ = [
    "convert_mov_to_mp4",
    "batch_convert_videos",
    "convert_heic_to_png",
    "batch_convert_images",
    "get_ffmpeg_path",
    "run_ffmpeg",
    "main",
]
