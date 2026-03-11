import os
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import generate_mondo, generate_mondo_enhanced
from scripts.seedream_client import build_payload, get_api_key, save_image_from_response


class BuildPayloadTests(unittest.TestCase):
    def test_build_payload_for_text_to_image_uses_defaults(self):
        payload = build_payload("poster prompt")

        self.assertEqual(payload["model"], "doubao-seedream-5-0-260128")
        self.assertEqual(payload["prompt"], "poster prompt")
        self.assertEqual(payload["size"], "2K")
        self.assertEqual(payload["output_format"], "png")
        self.assertFalse(payload["watermark"])
        self.assertNotIn("image", payload)


class ValidationTests(unittest.TestCase):
    def tearDown(self):
        output_path = Path("outputs/test-seedream.png")
        if output_path.exists():
            output_path.unlink()

    def test_get_api_key_raises_when_missing(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "ARK_API_KEY"):
                get_api_key()

    def test_build_payload_rejects_local_image_path(self):
        with self.assertRaisesRegex(ValueError, "remote image URL"):
            build_payload("poster prompt", image="poster.png")

    def test_save_image_from_response_writes_png_from_b64(self):
        response_data = {
            "data": [{"b64_json": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+yhZ0AAAAASUVORK5CYII="}]
        }

        output_path = save_image_from_response(response_data, "outputs/test-seedream.png")

        self.assertTrue(Path(output_path).exists())

    @patch("requests.get")
    def test_save_image_from_response_downloads_png_from_url(self, mock_get):
        mock_get.return_value.raise_for_status.return_value = None
        mock_get.return_value.content = b"png-bytes"
        response_data = {
            "data": [{"url": "https://example.com/test.png"}]
        }

        output_path = save_image_from_response(response_data, "outputs/test-seedream.png")

        self.assertTrue(Path(output_path).exists())
        self.assertEqual(Path(output_path).read_bytes(), b"png-bytes")


class IntegrationTests(unittest.TestCase):
    @patch("scripts.generate_mondo.generate_image")
    def test_generate_mondo_module_calls_shared_generate_image(self, mock_generate_image):
        prompt = generate_mondo.generate_prompt("Akira cyberpunk anime", "movie")
        generate_mondo.generate_image(prompt, aspect_ratio="9:16")

        mock_generate_image.assert_called_once()

    @patch("scripts.generate_mondo_enhanced.generate_image")
    def test_generate_mondo_enhanced_accepts_remote_url_input(self, mock_generate_image):
        prompt = generate_mondo_enhanced.generate_prompt("Blade Runner", "movie")
        remote_url = "https://example.com/poster.png"

        generate_mondo_enhanced.generate_image(prompt, aspect_ratio="9:16", input_image=remote_url)

        mock_generate_image.assert_called_once()
        self.assertEqual(mock_generate_image.call_args.kwargs["input_image"], remote_url)

    def test_generate_mondo_enhanced_rejects_local_input_path(self):
        with self.assertRaisesRegex(ValueError, "remote image URL"):
            generate_mondo_enhanced.generate_image(
                "poster prompt",
                aspect_ratio="9:16",
                input_image="poster.jpg",
            )


if __name__ == "__main__":
    unittest.main()
