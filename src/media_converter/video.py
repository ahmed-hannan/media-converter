"""Video conversion utilities (MOV to MP4)."""

import os
from pathlib import Path
from typing import List, Optional, Union

from .ffmpeg_utils import run_ffmpeg, FFmpegExecutionError


def convert_mov_to_mp4(
    input_path: Union[str, Path],
    output_path: Optional[Union[str, Path]] = None,
    crf: int = 23,
    preset: str = "medium",
    vcodec: str = "libx264",
    acodec: str = "aac",
    faststart: bool = True,
    overwrite: bool = True,
) -> Path:
    """
    Converts a QuickTime MOV file to an MP4 container.

    Args:
        input_path: Path to the input .mov file.
        output_path: Target path for the converted .mp4 file. Defaults to input path with .mp4 suffix.
        crf: Constant Rate Factor (0-51, lower means higher quality, default 23).
        preset: H.264 encoding preset (e.g. ultrafast, fast, medium, slow).
        vcodec: Video codec (default: libx264).
        acodec: Audio codec (default: aac).
        faststart: Enable '-movflags +faststart' for optimized web streaming.
        overwrite: Overwrite destination file if it exists.

    Returns:
        Path to the converted MP4 file.
    """
    source = Path(input_path).resolve()
    if not source.is_file():
        raise FileNotFoundError(f"Source video file not found: {source}")

    if output_path is None:
        target = source.with_suffix(".mp4")
    else:
        target = Path(output_path).resolve()

    target.parent.mkdir(parents=True, exist_ok=True)

    if target.is_file() and not overwrite:
        raise FileExistsError(f"Target file already exists: {target}")

    ffmpeg_args = []
    if overwrite:
        ffmpeg_args.append("-y")
    else:
        ffmpeg_args.append("-n")

    ffmpeg_args.extend(["-i", str(source)])
    ffmpeg_args.extend(["-c:v", vcodec, "-crf", str(crf), "-preset", preset, "-pix_fmt", "yuv420p"])
    ffmpeg_args.extend(["-c:a", acodec, "-b:a", "192k"])

    if faststart:
        ffmpeg_args.extend(["-movflags", "+faststart"])

    ffmpeg_args.append(str(target))

    run_ffmpeg(ffmpeg_args)
    return target


def batch_convert_videos(
    input_dir: Union[str, Path],
    output_dir: Optional[Union[str, Path]] = None,
    recursive: bool = False,
    crf: int = 23,
    preset: str = "medium",
    overwrite: bool = True,
) -> List[Path]:
    """
    Batch converts all MOV files in a directory to MP4.

    Args:
        input_dir: Directory containing .mov files.
        output_dir: Optional destination directory. If omitted, converted files remain alongside originals.
        recursive: Whether to scan subdirectories.
        crf: Quality factor.
        preset: Encoding preset.
        overwrite: Overwrite existing outputs.

    Returns:
        List of Path objects for newly converted MP4 files.
    """
    in_dir = Path(input_dir).resolve()
    if not in_dir.is_dir():
        raise NotADirectoryError(f"Input directory does not exist: {in_dir}")

    out_dir = Path(output_dir).resolve() if output_dir else None
    if out_dir:
        out_dir.mkdir(parents=True, exist_ok=True)

    pattern = "**/*.mov" if recursive else "*.mov"
    mov_files = list(in_dir.glob(pattern))

    converted: List[Path] = []
    for file_path in mov_files:
        if out_dir:
            relative_part = file_path.relative_to(in_dir)
            target = (out_dir / relative_part).with_suffix(".mp4")
        else:
            target = file_path.with_suffix(".mp4")

        converted_path = convert_mov_to_mp4(
            input_path=file_path,
            output_path=target,
            crf=crf,
            preset=preset,
            overwrite=overwrite,
        )
        converted.append(converted_path)

    return converted
