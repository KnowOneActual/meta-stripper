"""Core functionality for metadata stripping."""

from pathlib import Path
from typing import Optional, Dict, Any
from .handlers import get_handler


def display_metadata(filepath: Path) -> Optional[Dict[str, Any]]:
    """Display metadata from a file.
    
    Args:
        filepath: Path to the input file
        
    Returns:
        Dictionary of metadata key-value pairs, or None if no metadata found
    """
    handler = get_handler(filepath)
    return handler.display_metadata(filepath)


def strip_metadata(input_path: Path, output_path: Optional[Path] = None) -> Path:
    """Strip metadata from a file.
    
    Args:
        input_path: Path to the input file
        output_path: Optional path for output file. If not provided,
                    generates name with '_no_metadata' suffix
        
    Returns:
        Path to the created output file
        
    Raises:
        FileNotFoundError: If input file doesn't exist
        ValueError: If file type is unsupported
    """
    if not input_path.exists():
        raise FileNotFoundError(f"File not found: {input_path}")
    
    if output_path is None:
        stem = input_path.stem
        suffix = input_path.suffix
        output_path = input_path.parent / f"{stem}_no_metadata{suffix}"
    
    handler = get_handler(input_path)
    handler.strip_metadata(input_path, output_path)
    
    return output_path
