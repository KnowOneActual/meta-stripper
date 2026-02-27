# meta-stripper

Privacy-focused metadata removal tool for documents and images. Strip identifying information from PDFs, Office documents (Word, Excel, PowerPoint), images (JPEG, PNG, WebP), and more with a simple command.

[![Tests](https://github.com/KnowOneActual/meta-stripper/workflows/Tests/badge.svg)](https://github.com/KnowOneActual/meta-stripper/actions)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **⚠️ Project Status**: This is a concept project in early development stages. The tool is actively being developed and will be updated consistently. All feedback, suggestions, and contributions are welcome! Please open an [issue](https://github.com/KnowOneActual/meta-stripper/issues) or [discussion](https://github.com/KnowOneActual/meta-stripper/discussions) to share your thoughts.

## Documentation

- **📚 [Why Metadata Matters](WHY_METADATA_MATTERS.md)** - Comprehensive guide explaining metadata risks and why removal is critical for production workflows
- **⚡ [Quick Reference](QUICK_REFERENCE.md)** - One-page guide for common use cases and best practices
- **🗺️ [Roadmap](ROADMAP.md)** - Future features and version planning
- **🔒 [Security Policy](SECURITY.md)** - Security guidelines and vulnerability reporting
- **🤝 [Contributing](CONTRIBUTING.md)** - How to contribute to the project

## Features

- **PDF metadata removal** - Clean author, creator, producer, and custom fields
- **Microsoft Office support** - Strip metadata from Word (DOCX), Excel (XLSX), PowerPoint (PPTX)
- **JPEG EXIF removal** - Strip GPS, camera, and other EXIF data from photos
- **PNG metadata removal** - Clean text chunks and embedded metadata
- **WebP metadata removal** - Strip EXIF and XMP data from modern web images
- **Batch processing** - Handle multiple files at once
- **Cross-platform** - Works on Linux (Fedora) and macOS
- **Lightweight** - Minimal dependencies, fast execution
- **Safe defaults** - Creates new files, never modifies originals

## Installation

> **📦 Distribution Status**: This package is **not yet available on PyPI or Homebrew**. Holding off on public package distribution until the tool has been thoroughly tested. For now, please install from source.

### From Source (Current Method)

```bash
# Clone the repository
git clone https://github.com/KnowOneActual/meta-stripper.git
cd meta-stripper

# Install in development mode
pip install -e .

# Or install with dev dependencies
pip install -e ".[dev]"
```

### Future Installation Methods (v1.0.0+)

Once thoroughly tested, the following installation methods will be available:

```bash
# PyPI (coming soon)
pip install meta-stripper
pipx install meta-stripper

# Homebrew for macOS (planned)
brew install meta-stripper

# RPM for Fedora/RHEL (planned)
dnf install meta-stripper
```

See our [ROADMAP](ROADMAP.md) for the timeline toward v1.0.0 and public package distribution.

## Quick Start

```bash
# Strip metadata from documents
metastripper document.pdf report.xlsx presentation.pptx
metastripper contract.docx

# Strip EXIF data from photos
metastripper photo.jpg vacation.png modern_image.webp

# Process multiple files of different types
metastripper report.pdf photo.jpg spreadsheet.xlsx

# View metadata without stripping
metastripper --show document.xlsx
```

> 💡 **New to metadata removal?** Check out [Why Metadata Matters](WHY_METADATA_MATTERS.md) to understand the risks and [Quick Reference](QUICK_REFERENCE.md) for common usage patterns.

## Usage

### Basic Usage

```bash
# Strip metadata - creates document_no_metadata.pdf
metastripper document.pdf

# Strip from Excel - creates report_no_metadata.xlsx
metastripper report.xlsx

# Strip from PowerPoint - creates presentation_no_metadata.pptx
metastripper presentation.pptx

# Strip EXIF from photo - creates photo_no_metadata.jpg
metastripper photo.jpg

# Specify output filename
metastripper input.docx -o clean_output.docx

# View metadata before stripping
metastripper --show document.pdf
metastripper --show spreadsheet.xlsx
```

### Multiple Files

```bash
# Process multiple files of different types
metastripper file1.pdf file2.docx photo.jpg report.xlsx

# Use wildcards (bash)
metastripper *.pdf *.docx *.xlsx
metastripper *.jpg *.png *.webp
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

### Documents
- ✅ PDF (.pdf)
- ✅ Microsoft Word (.docx)
- ✅ Microsoft Excel (.xlsx)
- ✅ Microsoft PowerPoint (.pptx)

### Images  
- ✅ JPEG/JPG (.jpg, .jpeg)
- ✅ PNG (.png)
- ✅ WebP (.webp)

### Planned
- 🚧 HEIC/HEIF images - Under evaluation
- 🚧 LibreOffice (.odt, .ods, .odp) - Planned for v0.5.0

## How It Works

### PDF Files
Removes standard metadata fields including:
- Author
- Creator
- Producer
- Subject
- Title
- Keywords

### Office Files (DOCX, XLSX, PPTX)
Uses direct ZIP manipulation to:
- Remove `docProps/app.xml` (extended properties: application, company, manager)
- Clean `docProps/core.xml` (core properties: author, title, subject, keywords, dates)
- Remove `docProps/custom.xml` (custom properties)
- Preserve all document content, worksheets, slides, and formatting

**DOCX**: Preserves text, images, styles, headers/footers  
**XLSX**: Preserves all worksheets, formulas, charts, formatting  
**PPTX**: Preserves all slides, layouts, themes, animations, media

### JPEG/JPG Files
Removes EXIF metadata including:
- Camera make and model
- GPS location coordinates
- Date and time taken
- Software used
- Copyright information
- Thumbnail images
- Preserves image quality (95% JPEG quality)

### PNG Files
Removes metadata chunks including:
- Text chunks (tEXt, iTXt, zTXt)
- Creation time
- Author information
- Software information
- Embedded EXIF data (if present)
- Preserves transparency

### WebP Files
Removes metadata including:
- EXIF data (GPS, camera info, dates)
- XMP metadata
- ICC profiles (optional)
- Software information
- Preserves lossless/lossy format (90% quality for lossy)

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/KnowOneActual/meta-stripper.git
cd meta-stripper

# Checkout feature branch
git checkout feature/image-support

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
│       ├── __main__.py          # Entry point
│       ├── cli.py               # Command-line interface
│       ├── core.py              # Core functionality
│       └── handlers/
│           ├── __init__.py
│           ├── base.py          # Abstract handler
│           ├── pdf.py           # PDF handler
│           ├── docx.py          # Word handler
│           ├── xlsx.py          # Excel handler
│           ├── pptx.py          # PowerPoint handler
│           ├── jpeg.py          # JPEG handler
│           ├── png.py           # PNG handler
│           └── webp.py          # WebP handler
├── tests/                       # Test suite
├── pyproject.toml              # Project configuration
└── README.md
```

### Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Privacy & Security Notes

This tool removes **standard metadata fields** from documents and images. Please note:

- ✅ Removes author, title, creation dates, company, manager fields
- ✅ Removes EXIF, GPS, camera information from images
- ✅ Safe for common privacy use cases
- ❌ Does NOT remove steganographic data
- ❌ Does NOT strip watermarks or visual identifiers
- ❌ Does NOT guarantee complete anonymization
- ⚠️ JPEG processing may slightly reduce image quality (uses 95% quality setting)
- ⚠️ WebP processing uses 90% quality for lossy images

For maximum privacy, combine with other sanitization tools and manual review.

**Want to understand why metadata removal matters?** Read our comprehensive guide: [Why Metadata Matters](WHY_METADATA_MATTERS.md)

## Roadmap

- [x] Image format support (JPEG, PNG, WebP) - **v0.2.0**
- [x] Office format support (XLSX, PPTX) - **v0.2.0**
- [ ] HEIC/HEIF image support (evaluation in progress)
- [ ] Batch directory processing with `--recursive`
- [ ] In-place editing with `--in-place`
- [ ] Selective metadata preservation
- [ ] LibreOffice format support (ODT, ODS, ODP) - **v0.5.0**
- [ ] GUI for desktop users
- [ ] Homebrew formula for macOS
- [ ] RPM package for Fedora/RHEL

See [ROADMAP.md](ROADMAP.md) for detailed version planning.

## Testing & Feedback

We're currently in the testing phase before public distribution. If you:
- Find bugs → [Open an issue](https://github.com/KnowOneActual/meta-stripper/issues)
- Have feature ideas → [Start a discussion](https://github.com/KnowOneActual/meta-stripper/discussions)
- Want to contribute → See [CONTRIBUTING.md](CONTRIBUTING.md)

Your feedback helps make this tool better for everyone!

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

## Acknowledgments

- Inspired by [MAT2](https://0xacab.org/jvoisin/mat2) and other metadata removal tools
- Built with [PyPDF2](https://github.com/py-pdf/pypdf) for PDF handling
- Built with [Pillow](https://python-pillow.org/) for image handling

## Support

If you encounter issues or have questions:
- Open an issue: [GitHub Issues](https://github.com/KnowOneActual/meta-stripper/issues)
- Start a discussion: [GitHub Discussions](https://github.com/KnowOneActual/meta-stripper/discussions)
- See the [ROADMAP](ROADMAP.md) for planned features
