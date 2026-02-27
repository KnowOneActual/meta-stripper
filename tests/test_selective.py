"""Tests for selective metadata control."""

import pytest
import PyPDF2
from PIL import Image
from pathlib import Path
from metastripper.core import strip_metadata
from metastripper.handlers.pdf import PDFHandler
from metastripper.handlers.jpeg import JPEGHandler

@pytest.fixture
def pdf_with_multiple_metadata(tmp_path):
    """Create a PDF with multiple metadata fields."""
    filepath = tmp_path / "multi_meta.pdf"
    pdf_writer = PyPDF2.PdfWriter()
    pdf_writer.add_page(PyPDF2.PageObject.create_blank_page(width=612, height=792))
    pdf_writer.add_metadata({
        "/Author": "Author Name",
        "/Title": "Title Name",
        "/Subject": "Subject Name",
        "/CustomField": "Custom Value"
    })
    with filepath.open("wb") as f:
        pdf_writer.write(f)
    return filepath

def test_pdf_keep_fields(pdf_with_multiple_metadata, tmp_path):
    """Test keeping specific fields in PDF."""
    output_path = tmp_path / "keep_author.pdf"
    strip_metadata(pdf_with_multiple_metadata, output_path, keep_fields=["Author"])
    
    handler = PDFHandler()
    metadata = handler.display_metadata(output_path)
    
    assert metadata is not None
    assert metadata.get("Author") == "Author Name"
    assert "Title" not in metadata or metadata.get("Title") == ""
    assert "Subject" not in metadata or metadata.get("Subject") == ""
    assert "CustomField" not in metadata

def test_pdf_remove_fields(pdf_with_multiple_metadata, tmp_path):
    """Test removing specific fields in PDF."""
    output_path = tmp_path / "remove_title.pdf"
    strip_metadata(pdf_with_multiple_metadata, output_path, remove_fields=["Title"])
    
    handler = PDFHandler()
    metadata = handler.display_metadata(output_path)
    
    assert metadata is not None
    assert metadata.get("Author") == "Author Name"
    assert "Title" not in metadata or metadata.get("Title") == ""
    assert metadata.get("Subject") == "Subject Name"
    assert metadata.get("CustomField") == "Custom Value"

@pytest.fixture
def jpeg_with_exif(tmp_path):
    """Create a JPEG with EXIF metadata."""
    filepath = tmp_path / "test.jpg"
    img = Image.new("RGB", (100, 100), color="red")
    exif_data = img.getexif()
    exif_data[0x010F] = "Camera Maker" # Make
    exif_data[0x0110] = "Camera Model" # Model
    img.save(filepath, "JPEG", exif=exif_data)
    return filepath

def test_jpeg_keep_fields(jpeg_with_exif, tmp_path):
    """Test keeping specific EXIF fields."""
    output_path = tmp_path / "keep_make.jpg"
    strip_metadata(jpeg_with_exif, output_path, keep_fields=["Make"])
    
    handler = JPEGHandler()
    metadata = handler.display_metadata(output_path)
    
    assert metadata is not None
    assert metadata.get("Make") == "Camera Maker"
    assert "Model" not in metadata

def test_jpeg_remove_fields(jpeg_with_exif, tmp_path):
    """Test removing specific EXIF fields."""
    output_path = tmp_path / "remove_model.jpg"
    strip_metadata(jpeg_with_exif, output_path, remove_fields=["Model"])
    
    handler = JPEGHandler()
    metadata = handler.display_metadata(output_path)
    
    assert metadata is not None
    assert metadata.get("Make") == "Camera Maker"
    assert "Model" not in metadata
