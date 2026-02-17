"""File format handlers for metadata stripping."""

from pathlib import Path
from typing import Type
from .base import BaseHandler
from .pdf import PDFHandler
from .docx import DOCXHandler


HANDLER_MAP = {
    '.pdf': PDFHandler,
    '.docx': DOCXHandler,
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
        supported = ', '.join(HANDLER_MAP.keys())
        raise ValueError(
            f"Unsupported file type: {suffix}. "
            f"Supported types: {supported}"
        )
    
    return HANDLER_MAP[suffix]()


__all__ = ['BaseHandler', 'PDFHandler', 'DOCXHandler', 'get_handler']
