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

    def strip_metadata(
        self,
        input_path: Path,
        output_path: Path,
        keep_fields: Optional[list] = None,
        remove_fields: Optional[list] = None,
    ) -> None:
        """Strip metadata from a PNG file.

        Args:
            input_path: Path to input PNG file
            output_path: Path for output PNG file
            keep_fields: Optional list of fields to preserve
            remove_fields: Optional list of fields to explicitly remove

        Raises:
            Exception: If stripping fails
        """
        try:
            from PIL import PngImagePlugin

            with Image.open(input_path) as img:
                # Filter metadata if requested
                new_pnginfo = None
                if keep_fields or remove_fields:
                    new_pnginfo = PngImagePlugin.PngInfo()
                    if hasattr(img, "info") and img.info:
                        for key, value in img.info.items():
                            # Skip internal fields
                            if key in ("transparency", "gamma", "dpi", "icc_profile"):
                                continue

                            should_keep = False
                            if keep_fields:
                                if key.lower() in [f.lower() for f in keep_fields]:
                                    should_keep = True
                            elif remove_fields:
                                if key.lower() not in [f.lower() for f in remove_fields]:
                                    should_keep = True

                            if should_keep:
                                new_pnginfo.add_text(key, str(value))

                # Load image data
                if hasattr(img, "get_flattened_data"):
                    data = list(img.get_flattened_data())
                else:
                    data = list(img.getdata())

                # Create clean image
                clean_img = Image.new(img.mode, img.size)
                clean_img.putdata(data)

                # Save options
                save_kwargs = {
                    "format": "PNG",
                    "optimize": True,
                }

                if new_pnginfo:
                    save_kwargs["pnginfo"] = new_pnginfo

                # Preserve transparency if present
                if "transparency" in img.info:
                    save_kwargs["transparency"] = img.info["transparency"]

                clean_img.save(output_path, **save_kwargs)

        except Exception as e:
            raise Exception(f"Failed to strip PNG metadata: {e}") from e
