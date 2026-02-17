# meta-stripper

Privacy-focused metadata removal tool for documents. Strip identifying information from PDFs, DOCX files, and more with a simple command.

[![Tests](https://github.com/KnowOneActual/meta-stripper/workflows/Tests/badge.svg)](https://github.com/KnowOneActual/meta-stripper/actions)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- **PDF metadata removal** - Clean author, creator, producer, and custom fields
- **DOCX metadata stripping** - Remove document properties and custom XML
- **Batch processing** - Handle multiple files at once
- **Cross-platform** - Works on Linux (Fedora) and macOS
- **Lightweight** - Minimal dependencies, fast execution
- **Safe defaults** - Creates new files, never modifies originals

## Quick Start

```bash
# Install via pip
pip install meta-stripper

# Strip metadata from a single file
metastripper document.pdf

# Process multiple files
metastripper report.pdf contract.docx presentation.pptx

# View metadata without stripping
metastripper --show document.pdf
```

## Installation

### Using pipx (recommended for CLI tools)
```bash
pipx install meta-stripper
```

### Using pip
```bash
pip install meta-stripper
```

### From source
```bash
git clone https://github.com/KnowOneActual/meta-stripper.git
cd meta-stripper
pip install -e .
```

## Usage

### Basic Usage

```bash
# Strip metadata - creates document_no_metadata.pdf
metastripper document.pdf

# Specify output filename
metastripper input.docx -o clean_output.docx

# View metadata before stripping
metastripper --show document.pdf
```

### Multiple Files

```bash
# Process multiple files
metastripper file1.pdf file2.docx file3.pdf

# Use wildcards (bash)
metastripper *.pdf
```

### Options

```
usage: metastripper [-h] [-o OUTPUT] [-s] [-v] [--version] files [files ...]

positional arguments:
  files                 File(s) to process

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file path (only valid for single file input)
  -s, --show            Display metadata without stripping
  -v, --verbose         Enable verbose output
  --version             show program's version number and exit
```

## Supported Formats

- ✅ PDF (.pdf)
- ✅ Microsoft Word (.docx)
- 🚧 Images (JPEG, PNG) - Coming soon
- 🚧 LibreOffice (.odt, .ods) - Planned

## How It Works

### PDF Files
Removes standard metadata fields including:
- Author
- Creator
- Producer
- Subject
- Title
- Keywords

### DOCX Files
Uses direct ZIP manipulation to:
- Remove `docProps/app.xml` (extended properties)
- Clean `docProps/core.xml` (core properties)
- Remove `docProps/custom.xml` (custom properties)
- Preserve document content and formatting

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/KnowOneActual/meta-stripper.git
cd meta-stripper

# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Run tests with coverage
pytest tests/ --cov=src/metastripper --cov-report=term-missing
```

### Project Structure

```
meta-stripper/
├── src/
│   └── metastripper/
│       ├── __init__.py
│       ├── __main__.py          # Entry point for python -m metastripper
│       ├── cli.py               # Command-line interface
│       ├── core.py              # Core functionality
│       └── handlers/
│           ├── __init__.py
│           ├── base.py          # Abstract handler
│           ├── pdf.py           # PDF handler
│           └── docx.py          # DOCX handler
├── tests/                       # Test suite
├── pyproject.toml              # Project configuration
└── README.md
```

### Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Privacy & Security Notes

This tool removes **standard metadata fields** from documents. Please note:

- ✅ Removes author, title, creation dates, and similar metadata
- ✅ Safe for common privacy use cases
- ❌ Does NOT remove steganographic data
- ❌ Does NOT strip watermarks or visual identifiers
- ❌ Does NOT guarantee complete anonymization

For maximum privacy, combine with other sanitization tools and manual review.

## Roadmap

- [ ] Image format support (JPEG, PNG, WebP)
- [ ] Batch directory processing with `--recursive`
- [ ] In-place editing with `--in-place`
- [ ] Selective metadata preservation
- [ ] ODF format support (ODT, ODS)
- [ ] GUI for desktop users
- [ ] Homebrew formula for macOS
- [ ] RPM package for Fedora/RHEL

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

## Acknowledgments

- Inspired by [MAT2](https://0xacab.org/jvoisin/mat2) and other metadata removal tools
- Built with [PyPDF2](https://github.com/py-pdf/pypdf) for PDF handling

## Support

If you encounter issues or have questions:
- Open an issue: [GitHub Issues](https://github.com/KnowOneActual/meta-stripper/issues)
- Check the [documentation](https://github.com/KnowOneActual/meta-stripper)
