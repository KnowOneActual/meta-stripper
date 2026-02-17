"""Tests for core functionality."""

import pytest
from pathlib import Path
from metastripper.core import strip_metadata, display_metadata


def test_strip_metadata_file_not_found():
    """Test that FileNotFoundError is raised for non-existent file."""
    with pytest.raises(FileNotFoundError):
        strip_metadata(Path("nonexistent.pdf"))


def test_strip_metadata_unsupported_format(tmp_path):
    """Test that ValueError is raised for unsupported file types."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("test content")
    
    with pytest.raises(ValueError, match="Unsupported file type"):
        strip_metadata(test_file)
