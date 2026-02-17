"""Tests for file handlers."""

import pytest
from pathlib import Path
from metastripper.handlers import (
    get_handler,
    PDFHandler,
    DOCXHandler,
    XLSXHandler,
    PPTXHandler,
    JPEGHandler,
    PNGHandler,
    WebPHandler,
)


def test_get_handler_pdf():
    """Test that PDF handler is returned for .pdf files."""
    handler = get_handler(Path("test.pdf"))
    assert isinstance(handler, PDFHandler)


def test_get_handler_docx():
    """Test that DOCX handler is returned for .docx files."""
    handler = get_handler(Path("test.docx"))
    assert isinstance(handler, DOCXHandler)


def test_get_handler_xlsx():
    """Test that XLSX handler is returned for .xlsx files."""
    handler = get_handler(Path("test.xlsx"))
    assert isinstance(handler, XLSXHandler)


def test_get_handler_pptx():
    """Test that PPTX handler is returned for .pptx files."""
    handler = get_handler(Path("test.pptx"))
    assert isinstance(handler, PPTXHandler)


def test_get_handler_jpeg():
    """Test that JPEG handler is returned for .jpg files."""
    handler = get_handler(Path("test.jpg"))
    assert isinstance(handler, JPEGHandler)


def test_get_handler_jpeg_extension():
    """Test that JPEG handler is returned for .jpeg files."""
    handler = get_handler(Path("test.jpeg"))
    assert isinstance(handler, JPEGHandler)


def test_get_handler_png():
    """Test that PNG handler is returned for .png files."""
    handler = get_handler(Path("test.png"))
    assert isinstance(handler, PNGHandler)


def test_get_handler_webp():
    """Test that WebP handler is returned for .webp files."""
    handler = get_handler(Path("test.webp"))
    assert isinstance(handler, WebPHandler)


def test_get_handler_case_insensitive():
    """Test that handler detection is case-insensitive."""
    # Test uppercase extensions for documents
    handler_docx = get_handler(Path("test.DOCX"))
    assert isinstance(handler_docx, DOCXHandler)
    
    handler_xlsx = get_handler(Path("test.XLSX"))
    assert isinstance(handler_xlsx, XLSXHandler)
    
    handler_pptx = get_handler(Path("test.PPTX"))
    assert isinstance(handler_pptx, PPTXHandler)
    
    # Test uppercase extensions for images
    handler_jpg = get_handler(Path("test.JPG"))
    assert isinstance(handler_jpg, JPEGHandler)
    
    handler_png = get_handler(Path("test.PNG"))
    assert isinstance(handler_png, PNGHandler)
    
    handler_webp = get_handler(Path("test.WEBP"))
    assert isinstance(handler_webp, WebPHandler)


def test_get_handler_unsupported():
    """Test that ValueError is raised for unsupported formats."""
    with pytest.raises(ValueError, match="Unsupported file type"):
        get_handler(Path("test.txt"))
    
    with pytest.raises(ValueError, match="Unsupported file type"):
        get_handler(Path("test.gif"))
    
    with pytest.raises(ValueError, match="Unsupported file type"):
        get_handler(Path("test.bmp"))
    
    with pytest.raises(ValueError, match="Unsupported file type"):
        get_handler(Path("test.doc"))  # Old Office format
    
    with pytest.raises(ValueError, match="Unsupported file type"):
        get_handler(Path("test.xls"))  # Old Excel format
