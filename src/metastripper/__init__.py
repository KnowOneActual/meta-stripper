"""meta-stripper - Privacy-focused metadata removal tool for documents."""

__version__ = "0.1.0"
__author__ = "KnowOneActual"

from .core import strip_metadata, display_metadata

__all__ = ["strip_metadata", "display_metadata"]
