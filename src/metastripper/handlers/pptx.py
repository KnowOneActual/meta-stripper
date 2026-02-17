"""PPTX (PowerPoint) handler for metadata removal."""

import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path
from typing import Any, Dict, Optional

from .base import BaseHandler


class PPTXHandler(BaseHandler):
    """Handler for PPTX (PowerPoint) files.

    Uses ZIP manipulation to remove metadata from PowerPoint presentations
    while preserving all slide content, layouts, and formatting.
    """

    def display_metadata(self, filepath: Path) -> Optional[Dict[str, Any]]:
        """Display metadata from a PPTX file.

        Args:
            filepath: Path to the PPTX file

        Returns:
            Dictionary of metadata or None if no metadata found
        """
        metadata = {}

        try:
            with zipfile.ZipFile(filepath, "r") as zf:
                # Check for core properties
                if "docProps/core.xml" in zf.namelist():
                    core_xml = zf.read("docProps/core.xml")
                    root = ET.fromstring(core_xml)

                    # Common metadata fields
                    fields = {
                        "title": ".//{http://purl.org/dc/elements/1.1/}title",
                        "subject": ".//{http://purl.org/dc/elements/1.1/}subject",
                        "creator": ".//{http://purl.org/dc/elements/1.1/}creator",
                        "keywords": ".//{http://schemas.openxmlformats.org/package/2006/metadata/core-properties}keywords",
                        "description": ".//{http://purl.org/dc/elements/1.1/}description",
                        "lastModifiedBy": ".//{http://schemas.openxmlformats.org/package/2006/metadata/core-properties}lastModifiedBy",
                        "revision": ".//{http://schemas.openxmlformats.org/package/2006/metadata/core-properties}revision",
                        "created": ".//{http://purl.org/dc/terms/}created",
                        "modified": ".//{http://purl.org/dc/terms/}modified",
                    }

                    for field_name, xpath in fields.items():
                        elem = root.find(xpath)
                        if elem is not None and elem.text:
                            metadata[field_name] = elem.text

                # Check for app properties
                if "docProps/app.xml" in zf.namelist():
                    app_xml = zf.read("docProps/app.xml")
                    root = ET.fromstring(app_xml)

                    app_fields = {
                        "application": ".//{http://schemas.openxmlformats.org/officeDocument/2006/extended-properties}Application",
                        "appVersion": ".//{http://schemas.openxmlformats.org/officeDocument/2006/extended-properties}AppVersion",
                        "company": ".//{http://schemas.openxmlformats.org/officeDocument/2006/extended-properties}Company",
                        "presentationFormat": ".//{http://schemas.openxmlformats.org/officeDocument/2006/extended-properties}PresentationFormat",
                        "totalTime": ".//{http://schemas.openxmlformats.org/officeDocument/2006/extended-properties}TotalTime",
                    }

                    for field_name, xpath in app_fields.items():
                        elem = root.find(xpath)
                        if elem is not None and elem.text:
                            metadata[field_name] = elem.text

                # Check for custom properties
                if "docProps/custom.xml" in zf.namelist():
                    custom_xml = zf.read("docProps/custom.xml")
                    root = ET.fromstring(custom_xml)
                    custom_props = root.findall(
                        ".//{http://schemas.openxmlformats.org/officeDocument/2006/custom-properties}property"
                    )

                    for prop in custom_props:
                        name = prop.get("name")
                        value_elem = list(prop)[0] if len(prop) > 0 else None
                        if name and value_elem is not None:
                            metadata[f"custom_{name}"] = value_elem.text

            return metadata if metadata else None

        except Exception as e:
            raise Exception(f"Failed to read PPTX metadata: {e}") from e

    def strip_metadata(self, input_path: Path, output_path: Path) -> None:
        """Strip metadata from a PPTX file.

        Args:
            input_path: Path to input PPTX file
            output_path: Path for output PPTX file

        Raises:
            Exception: If stripping fails
        """
        try:
            with zipfile.ZipFile(input_path, "r") as zin, zipfile.ZipFile(
                output_path, "w", zipfile.ZIP_DEFLATED
            ) as zout:
                for item in zin.infolist():
                    # Skip metadata files
                    if item.filename in [
                        "docProps/app.xml",
                        "docProps/core.xml",
                        "docProps/custom.xml",
                    ]:
                        continue

                    # Copy all other files (slides, layouts, themes, media, etc.)
                    data = zin.read(item.filename)
                    zout.writestr(item, data)

        except Exception as e:
            raise Exception(f"Failed to strip PPTX metadata: {e}") from e
