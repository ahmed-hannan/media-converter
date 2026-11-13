"""FFmpeg discovery and subprocess execution utilities."""

import os
import shutil
import subprocess
from typing import List, Optional


class FFmpegNotFoundError(FileNotFoundError):
    """Raised when an FFmpeg executable cannot be located."""
    pass


class FFmpegExecutionError(RuntimeError):
    """Raised when FFmpeg execution fails."""
    pass


def get_ffmpeg_path() -> str:
    """
    Locates the FFmpeg executable.
    
    Resolution order:
    1. FFMPEG_PATH environment variable
    2. System PATH (via shutil.which)
    3. Bundled binary via imageio_ffmpeg
    """
    env_path = os.environ.get("FFMPEG_PATH")
    if env_path and os.path.isfile(env_path):
        return env_path

    which_path = shutil.which("ffmpeg")
    if which_path:
        return which_path

    try:
        import imageio_ffmpeg
        bundled = imageio_ffmpeg.get_ffmpeg_exe()
        if bundled and os.path.isfile(bundled):
            return bundled
    except ImportError:
        pass

    raise FFmpegNotFoundError(
        "FFmpeg binary not found. Please install FFmpeg on your system PATH "
        "or install imageio-ffmpeg ('pip install imageio-ffmpeg')."
    )


def run_ffmpeg(args: List[str], capture_output: bool = True) -> subprocess.CompletedProcess:
    """
    Runs FFmpeg with the provided CLI arguments.
    
    Args:
        args: List of command-line arguments (excluding the ffmpeg executable itself).
        capture_output: Whether to capture stdout/stderr in the completed process.
        
    Returns:
        subprocess.CompletedProcess instance.
        
    Raises:
        FFmpegExecutionError: If FFmpeg returns a non-zero exit code.
    """
    ffmpeg_exe = get_ffmpeg_path()
    command = [ffmpeg_exe] + args
    
    try:
        result = subprocess.run(
            command,
            capture_output=capture_output,
            text=True,
            check=False
        )
    except Exception as exc:
        raise FFmpegExecutionError(f"Failed to execute FFmpeg command: {exc}") from exc

    if result.returncode != 0:
        error_msg = result.stderr.strip() if result.stderr else f"Exit code {result.returncode}"
        raise FFmpegExecutionError(f"FFmpeg error: {error_msg}")

    return result
