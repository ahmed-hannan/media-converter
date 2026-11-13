"""Image conversion utilities (HEIC/HEIF to PNG)."""

import os
from pathlib import Path
from typing import List, Optional, Union

from PIL import Image, ImageOps
import pillow_heif


# Register HEIF opener with Pillow globally for transparent format handling
pillow_heif.register_heif_opener()


def convert_heic_to_png(
    input_path: Union[str, Path],
    output_path: Optional[Union[str, Path]] = None,
    auto_orient: bool = True,
    compress_level: int = 6,
    overwrite: bool = True,
) -> Path:
    """
    Converts a HEIC/HEIF image to PNG format.

    Args:
        input_path: Path to the input .heic or .heif file.
        output_path: Target path for the output .png file.
        auto_orient: Automatically orient image based on EXIF metadata.
        compress_level: Zlib compression level for PNG (0-9, default 6).
        overwrite: Overwrite destination file if it exists.

    Returns:
        Path to the converted PNG file.
    """
    source = Path(input_path).resolve()
    if not source.is_file():
        raise FileNotFoundError(f"Source image file not found: {source}")

    if output_path is None:
        target = source.with_suffix(".png")
    else:
        target = Path(output_path).resolve()

    target.parent.mkdir(parents=True, exist_ok=True)

    if target.is_file() and not overwrite:
        raise FileExistsError(f"Target file already exists: {target}")

    with Image.open(source) as img:
        if auto_orient:
            img = ImageOps.exif_transpose(img)

        # Preserve color fidelity and alpha channel
        if img.mode not in ("RGB", "RGBA"):
            img = img.convert("RGBA" if "A" in img.mode else "RGB")

        img.save(target, format="PNG", compress_level=compress_level)

    return target


def batch_convert_images(
    input_dir: Union[str, Path],
    output_dir: Optional[Union[str, Path]] = None,
    recursive: bool = False,
    auto_orient: bool = True,
    compress_level: int = 6,
    overwrite: bool = True,
) -> List[Path]:
    """
    Batch converts all HEIC/HEIF images in a directory to PNG.

    Args:
        input_dir: Directory containing .heic or .heif images.
        output_dir: Target output directory. If omitted, outputs are placed alongside inputs.
        recursive: Whether to search subdirectories.
        auto_orient: Correct image orientation via EXIF.
        compress_level: PNG compression level.
        overwrite: Overwrite existing output files.

    Returns:
        List of Path objects for converted PNG files.
    """
    in_dir = Path(input_dir).resolve()
    if not in_dir.is_dir():
        raise NotADirectoryError(f"Input directory does not exist: {in_dir}")

    out_dir = Path(output_dir).resolve() if output_dir else None
    if out_dir:
        out_dir.mkdir(parents=True, exist_ok=True)

    extensions = (".heic", ".HEIC", ".heif", ".HEIF")
    all_files = in_dir.rglob("*") if recursive else in_dir.glob("*")
    heic_files = [f for f in all_files if f.is_file() and f.suffix in extensions]

    converted: List[Path] = []
    for file_path in heic_files:
        if out_dir:
            relative_part = file_path.relative_to(in_dir)
            target = (out_dir / relative_part).with_suffix(".png")
        else:
            target = file_path.with_suffix(".png")

        result = convert_heic_to_png(
            input_path=file_path,
            output_path=target,
            auto_orient=auto_orient,
            compress_level=compress_level,
            overwrite=overwrite,
        )
        converted.append(result)

    return converted
