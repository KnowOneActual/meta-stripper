"""Tests for image file handlers (JPEG, PNG, WebP)."""

from pathlib import Path

import pytest
from PIL import Image

from metastripper.handlers import JPEGHandler, PNGHandler, WebPHandler


class TestJPEGHandler:
    """Tests for JPEG handler."""

    def test_display_metadata_with_exif(self, sample_jpeg_with_exif):
        """Test displaying EXIF metadata from JPEG."""
        handler = JPEGHandler()
        metadata = handler.display_metadata(sample_jpeg_with_exif)

        assert metadata is not None
        assert isinstance(metadata, dict)
        assert len(metadata) > 0

    def test_display_metadata_no_exif(self, sample_jpeg_no_metadata):
        """Test displaying metadata from JPEG without EXIF."""
        handler = JPEGHandler()
        metadata = handler.display_metadata(sample_jpeg_no_metadata)

        # Should return None or empty dict
        assert metadata is None or len(metadata) == 0

    def test_strip_metadata(self, sample_jpeg_with_exif, tmp_test_dir):
        """Test stripping metadata from JPEG."""
        handler = JPEGHandler()
        output_path = tmp_test_dir / "stripped_photo.jpg"

        # Strip metadata
        handler.strip_metadata(sample_jpeg_with_exif, output_path)

        # Verify output file exists
        assert output_path.exists()

        # Verify output has no/minimal EXIF data
        metadata_after = handler.display_metadata(output_path)
        assert metadata_after is None or len(metadata_after) == 0

        # Verify image is still valid
        img = Image.open(output_path)
        assert img.size == (100, 100)
        img.close()

    def test_strip_preserves_image_quality(self, sample_jpeg_with_exif, tmp_test_dir):
        """Test that stripping preserves reasonable image quality."""
        handler = JPEGHandler()
        output_path = tmp_test_dir / "stripped_quality.jpg"

        # Get original size
        original_size = sample_jpeg_with_exif.stat().st_size

        # Strip metadata
        handler.strip_metadata(sample_jpeg_with_exif, output_path)

        # Output should be similar size (within 50% tolerance)
        output_size = output_path.stat().st_size
        assert output_size > original_size * 0.5
        assert output_size < original_size * 1.5


class TestPNGHandler:
    """Tests for PNG handler."""

    def test_display_metadata_with_text(self, sample_png_with_metadata):
        """Test displaying text metadata from PNG."""
        handler = PNGHandler()
        metadata = handler.display_metadata(sample_png_with_metadata)

        assert metadata is not None
        assert isinstance(metadata, dict)
        assert len(metadata) > 0

    def test_display_metadata_no_text(self, sample_png_no_metadata):
        """Test displaying metadata from PNG without text chunks."""
        handler = PNGHandler()
        metadata = handler.display_metadata(sample_png_no_metadata)

        # Should return None or empty dict
        assert metadata is None or len(metadata) == 0

    def test_strip_metadata(self, sample_png_with_metadata, tmp_test_dir):
        """Test stripping metadata from PNG."""
        handler = PNGHandler()
        output_path = tmp_test_dir / "stripped_image.png"

        # Strip metadata
        handler.strip_metadata(sample_png_with_metadata, output_path)

        # Verify output file exists
        assert output_path.exists()

        # Verify output has no metadata
        metadata_after = handler.display_metadata(output_path)
        assert metadata_after is None or len(metadata_after) == 0

        # Verify image is still valid with transparency
        img = Image.open(output_path)
        assert img.size == (100, 100)
        assert img.mode == "RGBA"
        img.close()

    def test_strip_preserves_transparency(self, sample_png_with_metadata, tmp_test_dir):
        """Test that PNG transparency is preserved."""
        handler = PNGHandler()
        output_path = tmp_test_dir / "stripped_transparent.png"

        # Strip metadata
        handler.strip_metadata(sample_png_with_metadata, output_path)

        # Check transparency preserved
        img = Image.open(output_path)
        assert img.mode in ["RGBA", "LA", "P"]
        img.close()


class TestWebPHandler:
    """Tests for WebP handler."""

    def test_display_metadata_with_exif(self, sample_webp_with_exif):
        """Test displaying EXIF metadata from WebP."""
        handler = WebPHandler()
        metadata = handler.display_metadata(sample_webp_with_exif)

        assert metadata is not None
        assert isinstance(metadata, dict)
        assert len(metadata) > 0

    def test_strip_metadata(self, sample_webp_with_exif, tmp_test_dir):
        """Test stripping metadata from WebP."""
        handler = WebPHandler()
        output_path = tmp_test_dir / "stripped_image.webp"

        # Strip metadata
        handler.strip_metadata(sample_webp_with_exif, output_path)

        # Verify output file exists
        assert output_path.exists()

        # Verify output has no/minimal metadata
        metadata_after = handler.display_metadata(output_path)
        assert metadata_after is None or len(metadata_after) == 0

        # Verify image is still valid
        img = Image.open(output_path)
        assert img.size == (100, 100)
        img.close()

    def test_strip_preserves_format(self, sample_webp_with_exif, tmp_test_dir):
        """Test that WebP format is preserved."""
        handler = WebPHandler()
        output_path = tmp_test_dir / "stripped_format.webp"

        # Strip metadata
        handler.strip_metadata(sample_webp_with_exif, output_path)

        # Verify it's still a WebP
        img = Image.open(output_path)
        assert img.format == "WEBP"
        img.close()


class TestImageHandlersIntegration:
    """Integration tests for image handlers."""

    def test_multiple_strip_operations(self, sample_jpeg_with_exif, tmp_test_dir):
        """Test stripping metadata multiple times doesn't corrupt file."""
        handler = JPEGHandler()
        
        # First strip
        output1 = tmp_test_dir / "strip1.jpg"
        handler.strip_metadata(sample_jpeg_with_exif, output1)
        
        # Second strip
        output2 = tmp_test_dir / "strip2.jpg"
        handler.strip_metadata(output1, output2)
        
        # Both should be valid images
        img1 = Image.open(output1)
        img2 = Image.open(output2)
        
        assert img1.size == img2.size
        assert img1.mode == img2.mode
        
        img1.close()
        img2.close()

    def test_error_on_invalid_file(self, tmp_test_dir):
        """Test handlers raise proper errors on invalid files."""
        invalid_file = tmp_test_dir / "not_an_image.jpg"
        invalid_file.write_text("This is not an image")
        
        handler = JPEGHandler()
        
        with pytest.raises(Exception):
            handler.display_metadata(invalid_file)

    def test_error_on_nonexistent_file(self, tmp_test_dir):
        """Test handlers raise proper errors on nonexistent files."""
        nonexistent = tmp_test_dir / "does_not_exist.jpg"
        
        handler = JPEGHandler()
        
        with pytest.raises(Exception):
            handler.display_metadata(nonexistent)
