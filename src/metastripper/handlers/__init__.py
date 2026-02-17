"""File format handlers for metadata stripping."""

from pathlib import Path
from typing import Type
from .base import BaseHandler
from .pdf import PDFHandler
from .docx import DOCXHandler
from .jpeg import JPEGHandler
from .png import PNGHandler
from .webp import WebPHandler


HANDLER_MAP = {
    '.pdf': PDFHandler,
    '.docx': DOCXHandler,
    '.jpg': JPEGHandler,
    '.jpeg': JPEGHandler,
    '.png': PNGHandler,
    '.webp': WebPHandler,
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
        supported = ', '.join(sorted(set(HANDLER_MAP.keys())))
        raise ValueError(
            f"Unsupported file type: {suffix}. "
            f"Supported types: {supported}"
        )
    
    return HANDLER_MAP[suffix]()


__all__ = [
    'BaseHandler',
    'PDFHandler',
    'DOCXHandler',
    'JPEGHandler',
    'PNGHandler',
    'WebPHandler',
    'get_handler'
]
