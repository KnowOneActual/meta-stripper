"""Tests for Command-line interface."""

import os
import shutil
import zipfile
from pathlib import Path

import pytest
import PyPDF2
from PIL import Image

from metastripper.cli import get_files_to_process, main, parse_args, process_file


@pytest.fixture
def test_env(tmp_path):
    """Create a directory structure for testing CLI features."""
    test_dir = tmp_path / "test_env"
    test_dir.mkdir()
    (test_dir / "subdir1").mkdir()
    (test_dir / "subdir2" / "nested").mkdir(parents=True)

    # Create a valid PDF
    pdf_path = test_dir / "file1.pdf"
    pdf_writer = PyPDF2.PdfWriter()
    pdf_writer.add_page(PyPDF2.PageObject.create_blank_page(width=612, height=792))
    pdf_writer.add_metadata({"/Author": "Test Author"})
    with pdf_path.open("wb") as f:
        pdf_writer.write(f)

    # Create a valid DOCX (it's a zip)
    docx_path = test_dir / "subdir1" / "file2.docx"
    with zipfile.ZipFile(docx_path, "w") as zf:
        zf.writestr(
            "docProps/core.xml",
            '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"></cp:coreProperties>',
        )
        zf.writestr(
            "word/document.xml",
            '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body></w:body></w:document>',
        )

    # Create a valid JPEG
    jpg_path = test_dir / "subdir2" / "file3.jpg"
    img = Image.new("RGB", (100, 100), color="red")
    img.save(jpg_path, "JPEG")

    # Create a valid PNG
    png_path = test_dir / "subdir2" / "nested" / "file4.png"
    img = Image.new("RGBA", (100, 100), color="blue")
    img.save(png_path, "PNG")

    # Create some unsupported files to ensure they are ignored
    (test_dir / "ignore.txt").write_text("ignore me")

    return test_dir


def test_get_files_to_process(test_env):
    """Test recursive and non-recursive file discovery."""
    # Non-recursive
    files = get_files_to_process([test_env], recursive=False)
    assert len(files) == 0  # Only a directory was provided

    # Recursive
    files = get_files_to_process([test_env], recursive=True)
    assert len(files) == 4
    extensions = {f.suffix.lower() for f in files}
    assert extensions == {".pdf", ".docx", ".jpg", ".png"}

    # Specific file
    files = get_files_to_process([test_env / "file1.pdf"])
    assert len(files) == 1
    assert files[0].name == "file1.pdf"


def test_dry_run(test_env, capsys):
    """Test dry-run mode does not create files."""
    filepath = test_env / "file1.pdf"
    result = process_file(
        filepath, output_path=None, show_only=False, verbose=True, dry_run=True
    )
    assert result is True
    
    # Check output files
    no_metadata_files = list(test_env.rglob("*_no_metadata*"))
    assert len(no_metadata_files) == 0
    
    captured = capsys.readouterr()
    assert "[DRY-RUN] Processing:" in captured.out


def test_in_place_with_backup(test_env):
    """Test in-place processing with backup."""
    filepath = test_env / "file1.pdf"
    original_size = filepath.stat().st_size
    
    result = process_file(
        filepath, output_path=None, show_only=False, verbose=True, in_place=True, backup=True
    )
    assert result is True
    
    # Check that backup exists
    backup_path = filepath.with_suffix(filepath.suffix + ".bak")
    assert backup_path.exists()
    assert backup_path.stat().st_size == original_size
    
    # Check that original file still exists (it was replaced)
    assert filepath.exists()


def test_main_recursive(test_env, monkeypatch, capsys):
    """Test main function with recursive flag."""
    # Mock sys.argv
    monkeypatch.setattr("sys.argv", ["metastripper", "-r", str(test_env)])
    
    exit_code = main()
    assert exit_code == 0
    
    captured = capsys.readouterr()
    assert "Summary: 4/4 files processed successfully" in captured.out


def test_main_output_error(test_env, monkeypatch, capsys):
    """Test error when --output is used with multiple files."""
    # Multiple files + --output
    monkeypatch.setattr("sys.argv", ["metastripper", "-r", "-o", "out.pdf", str(test_env)])
    
    exit_code = main()
    assert exit_code == 1
    
    captured = capsys.readouterr()
    assert "Error: --output can only be used with a single input file" in captured.err


def test_main_in_place_output_error(test_env, monkeypatch, capsys):
    """Test error when --in-place and --output are used together."""
    filepath = str(test_env / "file1.pdf")
    monkeypatch.setattr("sys.argv", ["metastripper", filepath, "-i", "-o", "out.pdf"])
    
    exit_code = main()
    assert exit_code == 1
    
    captured = capsys.readouterr()
    assert "Error: --in-place and --output are mutually exclusive" in captured.err
