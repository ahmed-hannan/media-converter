import os
import shutil
import tempfile
import unittest
from pathlib import Path

from media_converter.ffmpeg_utils import get_ffmpeg_path, run_ffmpeg
from media_converter.video import convert_mov_to_mp4, batch_convert_videos


class TestVideoConverter(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.work_dir = Path(self.temp_dir)
        self.ffmpeg_exe = get_ffmpeg_path()

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

    def test_ffmpeg_detected(self):
        self.assertTrue(os.path.isfile(self.ffmpeg_exe))

    def test_single_mov_to_mp4(self):
        sample_mov = self._create_sample_mov("sample.mov")
        target_mp4 = self.work_dir / "converted.mp4"

        result = convert_mov_to_mp4(sample_mov, target_mp4)

        self.assertTrue(result.is_file())
        self.assertEqual(result, target_mp4)
        self.assertGreater(result.stat().st_size, 0)

    def test_single_mov_to_default_mp4_name(self):
        sample_mov = self._create_sample_mov("video_test.mov")
        result = convert_mov_to_mp4(sample_mov)

        expected_target = self.work_dir / "video_test.mp4"
        self.assertTrue(result.is_file())
        self.assertEqual(result, expected_target)

    def test_nonexistent_source_raises(self):
        non_existent = self.work_dir / "missing.mov"
        with self.assertRaises(FileNotFoundError):
            convert_mov_to_mp4(non_existent)

    def test_batch_convert_videos(self):
        mov1 = self._create_sample_mov("clip1.mov")
        mov2 = self._create_sample_mov("clip2.mov")

        out_dir = self.work_dir / "out"
        converted = batch_convert_videos(self.work_dir, out_dir)

        self.assertEqual(len(converted), 2)
        for c in converted:
            self.assertTrue(c.is_file())
            self.assertEqual(c.suffix, ".mp4")


if __name__ == "__main__":
    unittest.main()
