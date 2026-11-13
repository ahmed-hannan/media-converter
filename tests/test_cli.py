import io
import shutil
import tempfile
import unittest
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path

from PIL import Image
import pillow_heif

from media_converter.cli import main
from media_converter.ffmpeg_utils import run_ffmpeg


class TestCLI(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.work_dir = Path(self.temp_dir)
        pillow_heif.register_heif_opener()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _create_sample_mov(self, filename: str) -> Path:
        output_file = self.work_dir / filename
        cmd = [
            "-y",
            "-f", "lavfi",
            "-i", "testsrc=duration=0.5:size=160x120:rate=10",
            "-c:v", "prores",
            str(output_file)
        ]
        run_ffmpeg(cmd)
        return output_file

    def _create_sample_heic(self, filename: str) -> Path:
        output_file = self.work_dir / filename
        img = Image.new("RGB", (64, 64), color="yellow")
        img.save(output_file, format="HEIF")
        return output_file

    def test_cli_video_command(self):
        mov_path = self._create_sample_mov("clip.mov")
        out_mp4 = self.work_dir / "clip.mp4"

        out_buf = io.StringIO()
        with redirect_stdout(out_buf):
            ret = main(["video", str(mov_path), "-o", str(out_mp4)])

        self.assertEqual(ret, 0)
        self.assertTrue(out_mp4.is_file())
        self.assertIn("[SUCCESS]", out_buf.getvalue())

    def test_cli_image_command(self):
        heic_path = self._create_sample_heic("pic.heic")
        out_png = self.work_dir / "pic.png"

        out_buf = io.StringIO()
        with redirect_stdout(out_buf):
            ret = main(["image", str(heic_path), "-o", str(out_png)])

        self.assertEqual(ret, 0)
        self.assertTrue(out_png.is_file())
        self.assertIn("[SUCCESS]", out_buf.getvalue())

    def test_cli_batch_command(self):
        self._create_sample_mov("v1.mov")
        self._create_sample_heic("i1.heic")
        out_dir = self.work_dir / "converted_all"

        out_buf = io.StringIO()
        with redirect_stdout(out_buf):
            ret = main(["batch", str(self.work_dir), "-o", str(out_dir)])

        self.assertEqual(ret, 0)
        self.assertTrue((out_dir / "v1.mp4").is_file())
        self.assertTrue((out_dir / "i1.png").is_file())

    def test_cli_help(self):
        out_buf = io.StringIO()
        with redirect_stdout(out_buf):
            with self.assertRaises(SystemExit) as cm:
                main(["--help"])
        self.assertEqual(cm.exception.code, 0)
        self.assertIn("usage: media-convert", out_buf.getvalue())


if __name__ == "__main__":
    unittest.main()
