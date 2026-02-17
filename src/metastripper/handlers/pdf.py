"""PDF metadata handler."""

from pathlib import Path
from typing import Any, Dict, Optional

import PyPDF2

from .base import BaseHandler


class PDFHandler(BaseHandler):
    """Handler for PDF file metadata operations."""

    def display_metadata(self, filepath: Path) -> Optional[Dict[str, Any]]:
        """Display metadata from a PDF file.

        Args:
            filepath: Path to the PDF file

        Returns:
            Dictionary of metadata or None if no metadata found
        """
        try:
            with open(filepath, "rb") as f:
                pdf_reader = PyPDF2.PdfReader(f)
                metadata = pdf_reader.metadata

                if metadata:
                    # Clean up metadata keys (remove leading '/')
                    cleaned_metadata = {key.lstrip("/"): value for key, value in metadata.items()}
                    return cleaned_metadata
                return None

        except PyPDF2.errors.PdfReadError:
            raise ValueError(f"Could not read PDF file '{filepath}'. It may be corrupted.")
        except Exception as e:
            raise Exception(f"Error reading PDF metadata: {e}")

    def strip_metadata(self, input_path: Path, output_path: Path) -> None:
        """Strip metadata from a PDF file.

        Args:
            input_path: Path to input PDF
            output_path: Path for output PDF
        """
        try:
            with open(input_path, "rb") as f_in:
                pdf_reader = PyPDF2.PdfReader(f_in)
                pdf_writer = PyPDF2.PdfWriter()

                # Copy all pages
                for page in pdf_reader.pages:
                    pdf_writer.add_page(page)

                # Clear metadata by setting empty values
                pdf_writer.add_metadata(
                    {
                        "/Author": "",
                        "/Creator": "",
                        "/Producer": "",
                        "/Subject": "",
                        "/Title": "",
                        "/Keywords": "",
                    }
                )

                # Write cleaned PDF
                with open(output_path, "wb") as f_out:
                    pdf_writer.write(f_out)

        except Exception as e:
            raise Exception(f"Error stripping PDF metadata: {e}")
