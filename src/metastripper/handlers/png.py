"""PNG image handler for metadata removal."""

from pathlib import Path
from typing import Any, Dict, Optional

from PIL import Image

from .base import BaseHandler


class PNGHandler(BaseHandler):
    """Handler for PNG image files.

    Removes text chunks (tEXt, iTXt, zTXt) and other metadata from PNG images.
    """

    def display_metadata(self, filepath: Path) -> Optional[Dict[str, Any]]:
        """Display metadata from a PNG file.

        Args:
            filepath: Path to the PNG file

        Returns:
            Dictionary of metadata or None if no metadata found
        """
        try:
            with Image.open(filepath) as img:
                metadata = {}

                # PNG stores metadata in info dict
                if hasattr(img, "info") and img.info:
                    for key, value in img.info.items():
                        # Skip binary chunks we don't want to display
                        if key in ("transparency", "gamma", "dpi"):
                            continue

                        # Handle bytes data
                        if isinstance(value, bytes):
                            try:
                                value = value.decode("utf-8", errors="replace")
                            except Exception:
                                value = f"<binary data: {len(value)} bytes>"

                        metadata[key] = value

                # Also check for EXIF in PNG (less common but possible)
                if hasattr(img, "_getexif") and img._getexif():
                    from PIL.ExifTags import TAGS

                    exif_data = img._getexif()
                    for tag_id, value in exif_data.items():
                        tag_name = f"EXIF_{TAGS.get(tag_id, tag_id)}"
                        if isinstance(value, bytes):
                            try:
                                value = value.decode("utf-8", errors="replace")
                            except Exception:
                                value = f"<binary data: {len(value)} bytes>"
                        metadata[tag_name] = value

                return metadata if metadata else None

        except Exception as e:
            raise Exception(f"Failed to read PNG metadata: {e}") from e

    def strip_metadata(self, input_path: Path, output_path: Path) -> None:
        """Strip metadata from a PNG file.

        Args:
            input_path: Path to input PNG file
            output_path: Path for output PNG file

        Raises:
            Exception: If stripping fails
        """
        try:
            with Image.open(input_path) as img:
                # Create new image without metadata
                # Load image data using non-deprecated method
                data = list(img.get_flattened_data())

                # Create clean image with same mode and size
                clean_img = Image.new(img.mode, img.size)
                clean_img.putdata(data)

                # Save without metadata
                # PngInfo object would add metadata, so we don't use it
                save_kwargs = {
                    "format": "PNG",
                    "optimize": True,
                }

                # Preserve transparency if present (but not as metadata)
                if "transparency" in img.info:
                    save_kwargs["transparency"] = img.info["transparency"]

                clean_img.save(output_path, **save_kwargs)

        except Exception as e:
            raise Exception(f"Failed to strip PNG metadata: {e}") from e
