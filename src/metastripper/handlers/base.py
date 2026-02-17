"""Base handler class for metadata operations."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional


class BaseHandler(ABC):
    """Abstract base class for file format handlers."""

    @abstractmethod
    def display_metadata(self, filepath: Path) -> Optional[Dict[str, Any]]:
        """Display metadata from a file.

        Args:
            filepath: Path to the file

        Returns:
            Dictionary of metadata or None if no metadata found
        """

    @abstractmethod
    def strip_metadata(self, input_path: Path, output_path: Path) -> None:
        """Strip metadata from a file.

        Args:
            input_path: Path to input file
            output_path: Path for output file

        Raises:
            Exception: If stripping fails
        """
