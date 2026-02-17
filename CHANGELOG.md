# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned for v0.2.0
- Image format support (JPEG, PNG, WebP)
- Recursive directory processing
- Batch operation improvements

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
- GitHub Actions CI for automated testing
- Comprehensive documentation:
  - README with installation and usage examples
  - CONTRIBUTING guidelines
  - ROADMAP for future development
  - Privacy and security notes

### Technical Details
- Python 3.8+ compatibility
- Entry point script: `metastripper` command
- Support for `python -m metastripper` execution
- Safe defaults: Never modifies original files
- Auto-generated output filenames with `_no_metadata` suffix

[Unreleased]: https://github.com/KnowOneActual/meta-stripper/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/KnowOneActual/meta-stripper/releases/tag/v0.1.0
