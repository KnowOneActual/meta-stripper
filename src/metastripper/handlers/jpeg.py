"""JPEG/JPG image handler for EXIF metadata removal."""

from pathlib import Path
from typing import Any, Dict, Optional

from PIL import Image
from PIL.ExifTags import TAGS

from .base import BaseHandler


class JPEGHandler(BaseHandler):
    """Handler for JPEG/JPG image files.

    Removes EXIF metadata from JPEG images while preserving image quality.
    """

    def display_metadata(self, filepath: Path) -> Optional[Dict[str, Any]]:
        """Display EXIF metadata from a JPEG file.

        Args:
            filepath: Path to the JPEG file

        Returns:
            Dictionary of EXIF metadata or None if no metadata found
        """
        try:
            with Image.open(filepath) as img:
                exif_data = img._getexif()

                if not exif_data:
                    return None

                # Convert EXIF tag IDs to human-readable names
                metadata = {}
                for tag_id, value in exif_data.items():
                    tag_name = TAGS.get(tag_id, f"Unknown_{tag_id}")

                    # Handle bytes data
                    if isinstance(value, bytes):
                        try:
                            value = value.decode("utf-8", errors="replace")
                        except Exception:
                            value = f"<binary data: {len(value)} bytes>"

                    metadata[tag_name] = value

                return metadata

        except AttributeError:
            # Image has no EXIF data
            return None
        except Exception as e:
            raise Exception(f"Failed to read EXIF metadata: {e}") from e

    def strip_metadata(self, input_path: Path, output_path: Path) -> None:
        """Strip EXIF metadata from a JPEG file.

        Args:
            input_path: Path to input JPEG file
            output_path: Path for output JPEG file

        Raises:
            Exception: If stripping fails
        """
        try:
            with Image.open(input_path) as img:
                # Get image data without EXIF using non-deprecated method
                data = list(img.get_flattened_data())

                # Create new image without EXIF metadata
                # Convert to RGB if necessary (handles RGBA, LA, etc.)
                if img.mode not in ("RGB", "L"):
                    if img.mode == "RGBA":
                        # Create white background for transparency
                        background = Image.new("RGB", img.size, (255, 255, 255))
                        background.paste(img, mask=img.split()[3] if len(img.split()) > 3 else None)
                        img = background
                    else:
                        img = img.convert("RGB")

                # Create new image with same data but no metadata
                clean_img = Image.new(img.mode, img.size)
                clean_img.putdata(data)

                # Save without EXIF metadata
                # Quality=95 with optimize=False helps maintain file size
                clean_img.save(
                    output_path,
                    format="JPEG",
                    quality=95,
                    optimize=False,
                    exif=b"",  # Explicitly set empty EXIF
                )

        except Exception as e:
            raise Exception(f"Failed to strip JPEG metadata: {e}") from e
