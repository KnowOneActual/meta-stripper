"""WebP image handler for metadata removal."""

from pathlib import Path
from typing import Any, Dict, Optional

from PIL import Image
from PIL.ExifTags import TAGS

from .base import BaseHandler


class WebPHandler(BaseHandler):
    """Handler for WebP image files.

    Removes EXIF and XMP metadata from WebP images while preserving quality.
    """

    def display_metadata(self, filepath: Path) -> Optional[Dict[str, Any]]:
        """Display metadata from a WebP file.

        Args:
            filepath: Path to the WebP file

        Returns:
            Dictionary of metadata or None if no metadata found
        """
        try:
            with Image.open(filepath) as img:
                metadata = {}

                # Check for EXIF data
                try:
                    exif_data = img._getexif()
                    if exif_data:
                        for tag_id, value in exif_data.items():
                            tag_name = TAGS.get(tag_id, f"Unknown_{tag_id}")

                            # Handle bytes data
                            if isinstance(value, bytes):
                                try:
                                    value = value.decode("utf-8", errors="replace")
                                except:
                                    value = f"<binary data: {len(value)} bytes>"

                            metadata[f"EXIF_{tag_name}"] = value
                except (AttributeError, KeyError):
                    pass  # No EXIF data

                # Check for other metadata in info dict
                if hasattr(img, "info") and img.info:
                    for key, value in img.info.items():
                        # Skip binary chunks we don't want to display
                        if key in ("icc_profile", "transparency"):
                            continue

                        # Handle bytes data
                        if isinstance(value, bytes):
                            try:
                                value = value.decode("utf-8", errors="replace")
                            except:
                                value = f"<binary data: {len(value)} bytes>"

                        metadata[key] = value

                return metadata if metadata else None

        except Exception as e:
            raise Exception(f"Failed to read WebP metadata: {e}")

    def strip_metadata(self, input_path: Path, output_path: Path) -> None:
        """Strip metadata from a WebP file.

        Args:
            input_path: Path to input WebP file
            output_path: Path for output WebP file

        Raises:
            Exception: If stripping fails
        """
        try:
            with Image.open(input_path) as img:
                # Get image data without metadata
                data = list(img.getdata())

                # Create new image without metadata
                clean_img = Image.new(img.mode, img.size)
                clean_img.putdata(data)

                # Save without metadata
                # Quality=90 is a good balance for WebP (WebP is more efficient than JPEG)
                save_kwargs = {
                    "format": "WEBP",
                    "quality": 90,
                    "method": 6,  # Slowest but best compression
                    "exif": b"",  # Explicitly set empty EXIF
                }

                # Preserve lossless flag if it was lossless
                if hasattr(img, "info") and "lossless" in img.info:
                    save_kwargs["lossless"] = img.info["lossless"]

                clean_img.save(output_path, **save_kwargs)

        except Exception as e:
            raise Exception(f"Failed to strip WebP metadata: {e}")
