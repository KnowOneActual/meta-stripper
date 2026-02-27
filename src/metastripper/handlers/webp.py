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
                                except Exception:
                                    value = f"<binary data: {len(value)} bytes>"

                            metadata[f"EXIF_{tag_name}"] = value
                except (AttributeError, KeyError):
                    pass  # No EXIF data

                # Check for other metadata in info dict
                # Skip internal WebP properties that aren't user metadata
                if hasattr(img, "info") and img.info:
                    skip_keys = {"icc_profile", "transparency", "loop", "background", "duration"}
                    for key, value in img.info.items():
                        # Skip binary chunks and internal properties
                        if key in skip_keys:
                            continue

                        # Handle bytes data
                        if isinstance(value, bytes):
                            try:
                                value = value.decode("utf-8", errors="replace")
                            except Exception:
                                value = f"<binary data: {len(value)} bytes>"

                        metadata[key] = value

                return metadata if metadata else None

        except Exception as e:
            raise Exception(f"Failed to read WebP metadata: {e}") from e

    def strip_metadata(
        self,
        input_path: Path,
        output_path: Path,
        keep_fields: Optional[list] = None,
        remove_fields: Optional[list] = None,
    ) -> None:
        """Strip metadata from a WebP file.

        Args:
            input_path: Path to input WebP file
            output_path: Path for output WebP file
            keep_fields: Optional list of fields to preserve
            remove_fields: Optional list of fields to explicitly remove

        Raises:
            Exception: If stripping fails
        """
        try:
            with Image.open(input_path) as img:
                # Filter metadata if requested
                new_exif = None
                if keep_fields or remove_fields:
                    original_exif = img.getexif()
                    if original_exif:
                        new_exif = Image.Exif()
                        for tag_id, value in original_exif.items():
                            tag_name = TAGS.get(tag_id, str(tag_id))
                            
                            should_keep = False
                            if keep_fields:
                                if f"EXIF_{tag_name}".lower() in [f.lower() for f in keep_fields] or \
                                   tag_name.lower() in [f.lower() for f in keep_fields]:
                                    should_keep = True
                            elif remove_fields:
                                if f"EXIF_{tag_name}".lower() not in [f.lower() for f in remove_fields] and \
                                   tag_name.lower() not in [f.lower() for f in remove_fields]:
                                    should_keep = True
                            
                            if should_keep:
                                new_exif[tag_id] = value

                # Get image data without metadata
                if hasattr(img, "get_flattened_data"):
                    data = list(img.get_flattened_data())
                else:
                    data = list(img.getdata())

                # Create new image
                clean_img = Image.new(img.mode, img.size)
                clean_img.putdata(data)

                # Save without metadata
                save_kwargs = {
                    "format": "WEBP",
                    "quality": 90,
                    "method": 6,
                    "exif": new_exif if new_exif else b"",
                }

                # Preserve WebP-specific flags
                if hasattr(img, "info"):
                    for key in ("lossless", "icc_profile", "transparency", "loop", "background", "duration"):
                        if key in img.info:
                            save_kwargs[key] = img.info[key]

                clean_img.save(output_path, **save_kwargs)

        except Exception as e:
            raise Exception(f"Failed to strip WebP metadata: {e}") from e
