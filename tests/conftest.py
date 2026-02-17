"""Pytest configuration and shared fixtures."""

import io
from pathlib import Path

import pytest
from PIL import Image


@pytest.fixture
def tmp_test_dir(tmp_path):
    """Create a temporary directory for test files."""
    test_dir = tmp_path / "test_files"
    test_dir.mkdir()
    return test_dir


@pytest.fixture
def sample_jpeg_with_exif(tmp_test_dir):
    """Create a sample JPEG with EXIF metadata."""
    filepath = tmp_test_dir / "test_photo.jpg"
    
    # Create a simple image
    img = Image.new("RGB", (100, 100), color="red")
    
    # Add EXIF data
    exif_data = img.getexif()
    exif_data[0x010F] = "Test Camera"  # Make
    exif_data[0x0110] = "Test Model"   # Model
    exif_data[0x0131] = "Test Software"  # Software
    exif_data[0x013B] = "Test Author"  # Artist
    
    # Save with EXIF
    img.save(filepath, "JPEG", exif=exif_data, quality=95)
    
    return filepath


@pytest.fixture
def sample_png_with_metadata(tmp_test_dir):
    """Create a sample PNG with text metadata."""
    filepath = tmp_test_dir / "test_image.png"
    
    # Create a simple image
    img = Image.new("RGBA", (100, 100), color="blue")
    
    # Add metadata using PngInfo
    from PIL import PngImagePlugin
    pnginfo = PngImagePlugin.PngInfo()
    pnginfo.add_text("Author", "Test Author")
    pnginfo.add_text("Software", "Test Software")
    pnginfo.add_text("Comment", "Test Comment")
    
    # Save with metadata
    img.save(filepath, "PNG", pnginfo=pnginfo)
    
    return filepath


@pytest.fixture
def sample_webp_with_exif(tmp_test_dir):
    """Create a sample WebP with EXIF metadata."""
    filepath = tmp_test_dir / "test_image.webp"
    
    # Create a simple image
    img = Image.new("RGB", (100, 100), color="green")
    
    # Add EXIF data
    exif_data = img.getexif()
    exif_data[0x010F] = "Test Camera"  # Make
    exif_data[0x0131] = "Test Software"  # Software
    
    # Save with EXIF
    img.save(filepath, "WEBP", exif=exif_data, quality=90)
    
    return filepath


@pytest.fixture
def sample_jpeg_no_metadata(tmp_test_dir):
    """Create a JPEG without metadata."""
    filepath = tmp_test_dir / "clean_photo.jpg"
    img = Image.new("RGB", (100, 100), color="yellow")
    img.save(filepath, "JPEG", quality=95)
    return filepath


@pytest.fixture
def sample_png_no_metadata(tmp_test_dir):
    """Create a PNG without metadata."""
    filepath = tmp_test_dir / "clean_image.png"
    img = Image.new("RGBA", (100, 100), color="purple")
    img.save(filepath, "PNG")
    return filepath
