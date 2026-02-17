"""File format handlers for metadata stripping."""

from pathlib import Path
from typing import Type

from .base import BaseHandler
from .docx import DOCXHandler
from .jpeg import JPEGHandler
from .pdf import PDFHandler
from .png import PNGHandler
from .pptx import PPTXHandler
from .webp import WebPHandler
from .xlsx import XLSXHandler

HANDLER_MAP = {
    ".pdf": PDFHandler,
    ".docx": DOCXHandler,
    ".xlsx": XLSXHandler,
    ".pptx": PPTXHandler,
    ".jpg": JPEGHandler,
    ".jpeg": JPEGHandler,
    ".png": PNGHandler,
    ".webp": WebPHandler,
}


def get_handler(filepath: Path) -> Type[BaseHandler]:
    """Get appropriate handler for file type.

    Args:
        filepath: Path to file

    Returns:
        Handler class instance for the file type

    Raises:
        ValueError: If file type is unsupported
    """
    suffix = filepath.suffix.lower()

    if suffix not in HANDLER_MAP:
        supported = ", ".join(sorted(set(HANDLER_MAP.keys())))
        raise ValueError(f"Unsupported file type: {suffix}. " f"Supported types: {supported}")

    return HANDLER_MAP[suffix]()


__all__ = [
    "BaseHandler",
    "PDFHandler",
    "DOCXHandler",
    "XLSXHandler",
    "PPTXHandler",
    "JPEGHandler",
    "PNGHandler",
    "WebPHandler",
    "get_handler",
]
