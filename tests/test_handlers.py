"""Tests for file handlers."""

import pytest
from pathlib import Path
from metastripper.handlers import get_handler, PDFHandler, DOCXHandler


def test_get_handler_pdf():
    """Test that PDF handler is returned for .pdf files."""
    handler = get_handler(Path("test.pdf"))
    assert isinstance(handler, PDFHandler)


def test_get_handler_docx():
    """Test that DOCX handler is returned for .docx files."""
    handler = get_handler(Path("test.docx"))
    assert isinstance(handler, DOCXHandler)


def test_get_handler_unsupported():
    """Test that ValueError is raised for unsupported formats."""
    with pytest.raises(ValueError, match="Unsupported file type"):
        get_handler(Path("test.txt"))
