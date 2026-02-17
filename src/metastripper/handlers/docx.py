"""DOCX metadata handler."""

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Dict, Optional
from zipfile import ZIP_DEFLATED, ZipFile

from .base import BaseHandler


class DOCXHandler(BaseHandler):
    """Handler for DOCX file metadata operations."""

    def display_metadata(self, filepath: Path) -> Optional[Dict[str, Any]]:
        """Display metadata from a DOCX file.

        Args:
            filepath: Path to the DOCX file

        Returns:
            Dictionary of metadata or None if no metadata found
        """
        metadata = {}

        try:
            with ZipFile(filepath, "r") as zip_file:
                # Read core properties
                if "docProps/core.xml" in zip_file.namelist():
                    core_xml = zip_file.read("docProps/core.xml")
                    root = ET.fromstring(core_xml)

                    # Parse common metadata fields
                    ns = {
                        "dc": "http://purl.org/dc/elements/1.1/",
                        "dcterms": "http://purl.org/dc/terms/",
                        "cp": "http://schemas.openxmlformats.org/package/2006/metadata/core-properties",
                    }

                    fields = [
                        ("dc:creator", "Author"),
                        ("dc:title", "Title"),
                        ("dc:subject", "Subject"),
                        ("cp:lastModifiedBy", "Last Modified By"),
                        ("dcterms:created", "Created"),
                        ("dcterms:modified", "Modified"),
                    ]

                    for xml_field, display_name in fields:
                        elem = root.find(xml_field, ns)
                        if elem is not None and elem.text:
                            metadata[display_name] = elem.text

                # Check for app properties
                if "docProps/app.xml" in zip_file.namelist():
                    metadata["Has Extended Properties"] = "Yes"

                # Check for custom properties
                if "docProps/custom.xml" in zip_file.namelist():
                    metadata["Has Custom Properties"] = "Yes"

            return metadata if metadata else None

        except Exception as e:
            raise Exception(f"Error reading DOCX metadata: {e}") from e

    def strip_metadata(self, input_path: Path, output_path: Path) -> None:
        """Strip metadata from a DOCX file.

        Uses direct ZIP manipulation to avoid python-docx metadata issues.

        Args:
            input_path: Path to input DOCX
            output_path: Path for output DOCX
        """
        try:
            with ZipFile(input_path, "r") as zip_read, ZipFile(
                output_path, "w", ZIP_DEFLATED
            ) as zip_write:
                for item in zip_read.infolist():
                    filename = item.filename

                    # Remove app.xml (extended properties) completely
                    if filename == "docProps/app.xml":
                        continue

<<<<<<< Updated upstream
                    # Replace core.xml with clean version
                    if filename == "docProps/core.xml":
                        clean_core = self._create_clean_core_xml()
                        zip_write.writestr(item, clean_core)
                        continue

                    # Remove custom.xml if present
                    if filename == "docProps/custom.xml":
                        continue
=======
                        # Replace core.xml with clean version
                        if filename == "docProps/core.xml":
                            clean_core = self._create_clean_core_xml()
                            zip_write.writestr(item, clean_core)
                            continue

                        # Remove custom.xml if present
                        if filename == "docProps/custom.xml":
                            continue
>>>>>>> Stashed changes

                    # Copy everything else as-is
                    data = zip_read.read(filename)
                    zip_write.writestr(item, data)

        except Exception as e:
            raise Exception(f"Error stripping DOCX metadata: {e}") from e

    def _create_clean_core_xml(self) -> bytes:
        """Create minimal core.xml with no identifying metadata.

        Returns:
            Clean core.xml content as bytes
        """
        xml_lines = [
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">',
            "    <dc:creator></dc:creator>",
            "    <cp:revision>1</cp:revision>",
            '    <dcterms:created xsi:type="dcterms:W3CDTF">2020-01-01T00:00:00Z</dcterms:created>',
            '    <dcterms:modified xsi:type="dcterms:W3CDTF">2020-01-01T00:00:00Z</dcterms:modified>',
            "</cp:coreProperties>",
        ]

        return "\n".join(xml_lines).encode("utf-8")
