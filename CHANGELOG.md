# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## v0.2.1 - Testing & Tooling Upgrade

### Added
- New pytest fixtures for generating temporary test files (images and PDFs) to avoid checking in binary assets [web:110][web:116].
- Comprehensive tests for image handlers (JPEG, PNG, WebP), including:
  - Reading metadata from images with EXIF/text data.
  - Verifying metadata removal while preserving image dimensions and format.
  - Integration tests for repeated stripping and invalid/nonexistent inputs.
- Comprehensive tests for the PDF handler, including:
  - Metadata detection and key normalization (removal of leading `/`).
  - Metadata stripping while preserving page count and content.
  - Error handling for invalid and corrupted PDFs, aligned with PyPDF2’s metadata behavior (default `Producer` field) [web:106].

### Changed
- Relaxed tests to account for realistic behavior:
  - Allowing JPEG files to shrink after EXIF removal while still validating image integrity and dimensions [web:108][web:114].
  - Allowing harmless WebP runtime fields (such as `loop` and `background`) to remain after stripping, while ensuring EXIF/XMP-like data is removed [web:107][web:116].
  - Allowing PyPDF2’s default `Producer` metadata on PDFs that otherwise contain no user-supplied metadata [web:106].
- Updated Ruff configuration to use the new `[tool.ruff.lint]` section, resolving deprecation warnings in recent Ruff versions [web:113].

### Fixed
- Resolved all Ruff linting violations across the codebase, including:
  - Exception chaining (`B904`) by using `raise ... from e` / `from None`.
  - Removal of bare `except` clauses (`E722`) in favor of explicit `except Exception`.
  - Simplification of nested `with` statements (`SIM117`) and redundant branches (`RET505`, `RET507`).
  - Replacement of `open()` with `Path.open()` where appropriate (`PTH123`).
- Ensured handler modules and tests are fully Black/Ruff compliant and integrated into pre-commit hooks [web:124][web:123].

### Quality & CI
- Increased effective test coverage from minimal handler-registration tests to meaningful behavioral coverage across PDF and image handlers, with overall coverage now above the configured threshold.
- Kept coverage threshold at a realistic level while the test suite is expanded, preventing false negatives in CI while still enforcing a minimum quality bar [web:126].




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

[Unreleased]: https://github.com/KnowOneActual/meta-stripper/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/KnowOneActual/meta-stripper/releases/tag/v0.1.0
