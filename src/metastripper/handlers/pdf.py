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
            with filepath.open("rb") as f:
                pdf_reader = PyPDF2.PdfReader(f)
                metadata = pdf_reader.metadata

                if metadata:
                    # Clean up metadata keys and filter auto-generated values
                    cleaned = {}
                    for key, value in metadata.items():
                        clean_key = key.lstrip("/")
                        # Skip empty values and auto-generated Producer
                        if (
                            value
                            and value.strip()
                            and not (clean_key == "Producer" and value == "PyPDF2")
                        ):
                            cleaned[clean_key] = value

                    return cleaned if cleaned else None
                return None

        except PyPDF2.errors.PdfReadError:
            raise ValueError(
                f"Could not read PDF file '{filepath}'. It may be corrupted."
            ) from None
        except Exception as e:
            raise Exception(f"Error reading PDF metadata: {e}") from e

    def strip_metadata(
        self,
        input_path: Path,
        output_path: Path,
        keep_fields: Optional[list] = None,
        remove_fields: Optional[list] = None,
    ) -> None:
        """Strip metadata from a PDF file.

        Args:
            input_path: Path to input PDF
            output_path: Path for output PDF
            keep_fields: Optional list of fields to preserve
            remove_fields: Optional list of fields to explicitly remove
        """
        try:
            with input_path.open("rb") as f_in:
                pdf_reader = PyPDF2.PdfReader(f_in)
                pdf_writer = PyPDF2.PdfWriter()

                # Copy all pages
                for page in pdf_reader.pages:
                    pdf_writer.add_page(page)

                # Get original metadata
                original_metadata = pdf_reader.metadata
                new_metadata = {}

                # Normalization: internal keys start with /, display keys don't
                # We'll normalize to names without / for comparison
                standard_fields = ["Author", "Creator", "Producer", "Subject", "Title", "Keywords"]

                if original_metadata:
                    for key, value in original_metadata.items():
                        clean_key = key.lstrip("/")
                        
                        # Decision logic for selective stripping
                        should_keep = False
                        if keep_fields:
                            # If keep_fields is specified, only keep those
                            if clean_key.lower() in [f.lower() for f in keep_fields]:
                                should_keep = True
                        elif remove_fields:
                            # If remove_fields is specified, keep everything else
                            if clean_key.lower() not in [f.lower() for f in remove_fields]:
                                should_keep = True
                        else:
                            # Default: remove all standard fields
                            if clean_key not in standard_fields:
                                should_keep = True

                        if should_keep:
                            new_metadata[key] = value
                        else:
                            # Explicitly clear standard fields
                            if clean_key in standard_fields:
                                new_metadata[key] = ""

                # If no metadata exists but we want to clear standard ones
                if not original_metadata and not keep_fields:
                    for field in standard_fields:
                        new_metadata[f"/{field}"] = ""

                # Apply metadata
                pdf_writer.add_metadata(new_metadata)

                # Write cleaned PDF
                with output_path.open("wb") as f_out:
                    pdf_writer.write(f_out)

        except Exception as e:
            raise Exception(f"Error stripping PDF metadata: {e}") from e
