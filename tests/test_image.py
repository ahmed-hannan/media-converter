import shutil
import tempfile
import unittest
from pathlib import Path

from PIL import Image
import pillow_heif

from media_converter.image import convert_heic_to_png, batch_convert_images


class TestImageConverter(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.work_dir = Path(self.temp_dir)
        pillow_heif.register_heif_opener()

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _create_sample_heic(self, filename: str, size=(120, 80), color="blue") -> Path:
        output_file = self.work_dir / filename
        img = Image.new("RGB", size, color=color)
        img.save(output_file, format="HEIF")
        return output_file

    def test_single_heic_to_png(self):
        sample = self._create_sample_heic("test.heic", size=(200, 100), color="green")
        target_png = self.work_dir / "converted.png"

        result = convert_heic_to_png(sample, target_png)

        self.assertTrue(result.is_file())
        self.assertEqual(result, target_png)

        with Image.open(result) as out_img:
            self.assertEqual(out_img.size, (200, 100))
            self.assertEqual(out_img.format, "PNG")

    def test_default_output_path(self):
        sample = self._create_sample_heic("photo.heic")
        result = convert_heic_to_png(sample)

        expected = self.work_dir / "photo.png"
        self.assertTrue(result.is_file())
        self.assertEqual(result, expected)

    def test_missing_input_raises(self):
        missing = self.work_dir / "does_not_exist.heic"
        with self.assertRaises(FileNotFoundError):
            convert_heic_to_png(missing)

    def test_batch_convert_images(self):
        img1 = self._create_sample_heic("photo1.heic")
        img2 = self._create_sample_heic("photo2.heif")

        out_dir = self.work_dir / "out"
        converted = batch_convert_images(self.work_dir, out_dir)

        self.assertEqual(len(converted), 2)
        for c in converted:
            self.assertTrue(c.is_file())
            self.assertEqual(c.suffix, ".png")


if __name__ == "__main__":
    unittest.main()
