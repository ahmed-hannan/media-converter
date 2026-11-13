"""Command-line interface for media-converter."""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from .video import convert_mov_to_mp4, batch_convert_videos
from .image import convert_heic_to_png, batch_convert_images


def build_parser() -> argparse.ArgumentParser:
    """Constructs the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="media-convert",
        description="Convert MOV videos to MP4 and HEIC images to PNG.",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Video subcommand
    vid_parser = subparsers.add_parser("video", help="Convert a MOV file to MP4")
    vid_parser.add_argument("input", type=str, help="Path to input .mov file")
    vid_parser.add_argument("-o", "--output", type=str, default=None, help="Output .mp4 file path")
    vid_parser.add_argument("--crf", type=int, default=23, help="Constant rate factor (0-51, default: 23)")
    vid_parser.add_argument("--preset", type=str, default="medium", help="Encoding preset (default: medium)")
    vid_parser.add_argument("--no-faststart", action="store_true", help="Disable web faststart flag")

    # Image subcommand
    img_parser = subparsers.add_parser("image", help="Convert a HEIC/HEIF image to PNG")
    img_parser.add_argument("input", type=str, help="Path to input .heic file")
    img_parser.add_argument("-o", "--output", type=str, default=None, help="Output .png file path")
    img_parser.add_argument("--no-orient", action="store_true", help="Disable automatic EXIF orientation")
    img_parser.add_argument("--compress-level", type=int, default=6, help="PNG compression level 0-9 (default: 6)")

    # Batch subcommand
    batch_parser = subparsers.add_parser("batch", help="Batch convert files in a directory")
    batch_parser.add_argument("input_dir", type=str, help="Input directory containing files")
    batch_parser.add_argument("-o", "--output-dir", type=str, default=None, help="Output directory")
    batch_parser.add_argument(
        "--type",
        choices=["all", "video", "image"],
        default="all",
        help="Type of files to convert (default: all)",
    )
    batch_parser.add_argument("-r", "--recursive", action="store_true", help="Scan subdirectories recursively")

    return parser


def handle_video(args: argparse.Namespace) -> int:
    """Executes video conversion from CLI arguments."""
    try:
        out = convert_mov_to_mp4(
            input_path=args.input,
            output_path=args.output,
            crf=args.crf,
            preset=args.preset,
            faststart=not args.no_faststart,
        )
        print(f"[SUCCESS] Video converted: {out}")
        return 0
    except Exception as exc:
        print(f"[ERROR] Video conversion failed: {exc}", file=sys.stderr)
        return 1


def handle_image(args: argparse.Namespace) -> int:
    """Executes image conversion from CLI arguments."""
    try:
        out = convert_heic_to_png(
            input_path=args.input,
            output_path=args.output,
            auto_orient=not args.no_orient,
            compress_level=args.compress_level,
        )
        print(f"[SUCCESS] Image converted: {out}")
        return 0
    except Exception as exc:
        print(f"[ERROR] Image conversion failed: {exc}", file=sys.stderr)
        return 1


def handle_batch(args: argparse.Namespace) -> int:
    """Executes batch conversion from CLI arguments."""
    failures = 0
    in_dir = Path(args.input_dir)
    if not in_dir.is_dir():
        print(f"[ERROR] Specified directory does not exist: {in_dir}", file=sys.stderr)
        return 1

    if args.type in ("all", "video"):
        print(f"Scanning for MOV files in {in_dir}...")
        try:
            converted_videos = batch_convert_videos(
                input_dir=in_dir,
                output_dir=args.output_dir,
                recursive=args.recursive,
            )
            print(f"[SUCCESS] Converted {len(converted_videos)} video(s).")
        except Exception as exc:
            print(f"[ERROR] Video batch conversion error: {exc}", file=sys.stderr)
            failures += 1

    if args.type in ("all", "image"):
        print(f"Scanning for HEIC files in {in_dir}...")
        try:
            converted_images = batch_convert_images(
                input_dir=in_dir,
                output_dir=args.output_dir,
                recursive=args.recursive,
            )
            print(f"[SUCCESS] Converted {len(converted_images)} image(s).")
        except Exception as exc:
            print(f"[ERROR] Image batch conversion error: {exc}", file=sys.stderr)
            failures += 1

    return 1 if failures > 0 else 0


def main(argv: Optional[List[str]] = None) -> int:
    """CLI entry point."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 1

    if args.command == "video":
        return handle_video(args)
    elif args.command == "image":
        return handle_image(args)
    elif args.command == "batch":
        return handle_batch(args)

    return 0


if __name__ == "__main__":
    sys.exit(main())
