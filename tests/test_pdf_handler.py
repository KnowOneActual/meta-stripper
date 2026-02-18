"""Tests for PDF file handler."""

import PyPDF2
import pytest

from metastripper.handlers import PDFHandler


@pytest.fixture
def sample_pdf_with_metadata(tmp_path):
    """Create a sample PDF with metadata."""
    filepath = tmp_path / "test_document.pdf"

    # Create a PDF with metadata
    pdf_writer = PyPDF2.PdfWriter()

    # Add a blank page
    page = PyPDF2.PageObject.create_blank_page(width=612, height=792)
    pdf_writer.add_page(page)

    # Add metadata
    pdf_writer.add_metadata(
        {
            "/Author": "Test Author",
            "/Creator": "Test Creator",
            "/Producer": "Test Producer",
            "/Subject": "Test Subject",
            "/Title": "Test Title",
            "/Keywords": "test, metadata, privacy",
        }
    )

    # Write to file
    with filepath.open("wb") as f:
        pdf_writer.write(f)

    return filepath


@pytest.fixture
def sample_pdf_no_metadata(tmp_path):
    """Create a sample PDF without metadata."""
    filepath = tmp_path / "clean_document.pdf"

    # Create a PDF without metadata
    pdf_writer = PyPDF2.PdfWriter()

    # Add a blank page
    page = PyPDF2.PageObject.create_blank_page(width=612, height=792)
    pdf_writer.add_page(page)

    # Write without metadata
    with filepath.open("wb") as f:
        pdf_writer.write(f)

    return filepath


class TestPDFHandler:
    """Tests for PDF handler."""

    def test_display_metadata_with_data(self, sample_pdf_with_metadata):
        """Test displaying metadata from PDF with metadata."""
        handler = PDFHandler()
        metadata = handler.display_metadata(sample_pdf_with_metadata)

        assert metadata is not None
        assert isinstance(metadata, dict)
        assert "Author" in metadata or "Title" in metadata
        assert len(metadata) > 0

    def test_display_metadata_no_data(self, sample_pdf_no_metadata):
        """Test displaying metadata from PDF without metadata."""
        handler = PDFHandler()
        metadata = handler.display_metadata(sample_pdf_no_metadata)

        # Should return None or empty dict
        assert metadata is None or len(metadata) == 0

    def test_strip_metadata(self, sample_pdf_with_metadata, tmp_path):
        """Test stripping metadata from PDF."""
        handler = PDFHandler()
        output_path = tmp_path / "stripped_document.pdf"

        # Strip metadata
        handler.strip_metadata(sample_pdf_with_metadata, output_path)

        # Verify output file exists
        assert output_path.exists()

        # Verify output has no meaningful metadata
        metadata_after = handler.display_metadata(output_path)

        # Check that metadata is cleared (empty strings)
        if metadata_after:
            for key, value in metadata_after.items():
                assert value == "" or value is None, f"Metadata {key} not cleared: {value}"

    def test_strip_preserves_content(self, sample_pdf_with_metadata, tmp_path):
        """Test that stripping preserves PDF content."""
        handler = PDFHandler()
        output_path = tmp_path / "stripped_content.pdf"

        # Get original page count
        with sample_pdf_with_metadata.open("rb") as f:
            original_pdf = PyPDF2.PdfReader(f)
            original_pages = len(original_pdf.pages)

        # Strip metadata
        handler.strip_metadata(sample_pdf_with_metadata, output_path)

        # Verify page count preserved
        with output_path.open("rb") as f:
            stripped_pdf = PyPDF2.PdfReader(f)
            stripped_pages = len(stripped_pdf.pages)

        assert original_pages == stripped_pages

    def test_strip_multiple_pages(self, tmp_path):
        """Test stripping metadata from multi-page PDF."""
        # Create multi-page PDF
        filepath = tmp_path / "multi_page.pdf"
        pdf_writer = PyPDF2.PdfWriter()

        # Add multiple pages
        for _i in range(5):
            page = PyPDF2.PageObject.create_blank_page(width=612, height=792)
            pdf_writer.add_page(page)

        # Add metadata
        pdf_writer.add_metadata({"/Author": "Test", "/Title": "Multi-page Test"})

        with filepath.open("wb") as f:
            pdf_writer.write(f)

        # Strip metadata
        handler = PDFHandler()
        output_path = tmp_path / "stripped_multi.pdf"
        handler.strip_metadata(filepath, output_path)

        # Verify 5 pages still exist
        with output_path.open("rb") as f:
            pdf = PyPDF2.PdfReader(f)
            assert len(pdf.pages) == 5

    def test_error_on_invalid_pdf(self, tmp_path):
        """Test handler raises error on invalid PDF."""
        invalid_file = tmp_path / "not_a_pdf.pdf"
        invalid_file.write_text("This is not a PDF")

        handler = PDFHandler()

        with pytest.raises((ValueError, Exception)):
            handler.display_metadata(invalid_file)

    def test_error_on_corrupted_pdf(self, tmp_path):
        """Test handler raises error on corrupted PDF."""
        corrupted_file = tmp_path / "corrupted.pdf"
        corrupted_file.write_bytes(b"%PDF-1.4\nCorrupted data here")

        handler = PDFHandler()

        with pytest.raises((ValueError, Exception)):
            handler.display_metadata(corrupted_file)

    def test_metadata_keys_cleaned(self, sample_pdf_with_metadata):
        """Test that metadata keys have leading '/' removed."""
        handler = PDFHandler()
        metadata = handler.display_metadata(sample_pdf_with_metadata)

        if metadata:
            # All keys should not start with '/'
            for key in metadata:
                assert not key.startswith("/"), f"Key still has '/': {key}"
