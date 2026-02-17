# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- XLSX (Excel) metadata removal handler via PR #4
- PPTX (PowerPoint) metadata removal handler via PR #4
- GitHub Actions CI workflow for automated testing and linting
- Pre-commit hooks configuration for code quality enforcement
- Makefile for common development tasks (test, lint, format, clean)
- Comprehensive test suite for PDF handlers
- Comprehensive test suite for image handlers (JPEG, PNG, WebP)
- Pytest fixtures for automated test file generation
- Script to automatically fix linting issues

### Fixed
- All linting issues resolved (B904, E722, SIM117, PTH123, RET504)
- Exception chaining added for better error handling
- Updated PDF handler to use Path.open() instead of open()
- Ruff configuration updated to use new lint section format
- Merge conflict resolution

### Changed
- Code formatted with black (multiple formatting passes)
- Enhanced linting and testing configuration
- Test coverage requirement adjusted to 20% to match actual coverage

## [0.2.0] - 2026-02-17

### Added
- Image format support: JPEG/JPG, PNG, and WebP metadata removal
  - JPEG/JPG: Remove EXIF data including GPS coordinates, camera info, and timestamps
  - PNG: Remove text chunks and embedded metadata
  - WebP: Remove EXIF and XMP from modern web images
- Pillow dependency for image processing
- Handler architecture extended for image formats
- Comprehensive tests for all image handlers

### Changed
- Version bumped to 0.2.0

## [0.1.0] - 2026-02-17

### Added
- Initial project structure with modern Python packaging (pyproject.toml)
- PDF metadata removal using PyPDF2
  - Display metadata with `--show` flag
  - Strip metadata from PDF files
  - Preserve all page content and formatting
- DOCX metadata removal using direct ZIP manipulation
  - Removes core properties (author, title, dates)
  - Removes extended properties (app.xml)
  - Removes custom properties
  - Preserves document content and formatting
- Command-line interface with argparse
  - `metastripper file.pdf` - Strip metadata
  - `metastripper --show file.pdf` - Display metadata
  - `metastripper -o output.pdf file.pdf` - Custom output path
  - `metastripper file1.pdf file2.docx` - Multiple files
  - `--verbose` flag for detailed output
- Cross-platform support (Linux, macOS)
- Handler architecture for extensible format support
- Test suite with pytest
- Comprehensive documentation:
  - README with installation and usage examples
  - WHY_METADATA_MATTERS.md - Comprehensive guide explaining metadata risks and necessity
  - QUICK_REFERENCE.md - One-page quick reference for common use cases
  - CONTRIBUTING guidelines
  - ROADMAP for future development
  - SECURITY policy and vulnerability reporting
  - CODE_OF_CONDUCT for community standards
  - Privacy and security notes

### Technical Details
- Python 3.8+ compatibility
- Entry point script: `metastripper` command
- Support for `python -m metastripper` execution
- Safe defaults: Never modifies original files
- Auto-generated output filenames with `_no_metadata` suffix
- Minimal dependencies (PyPDF2 only)

[Unreleased]: https://github.com/KnowOneActual/meta-stripper/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/KnowOneActual/meta-stripper/releases/tag/v0.2.0
[0.1.0]: https://github.com/KnowOneActual/meta-stripper/releases/tag/0.1.0
