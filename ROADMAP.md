# meta-stripper Roadmap

This document outlines the planned features and development priorities for meta-stripper.

## Version 0.1.0 (Initial Release) ✅

**Status**: In Progress (PR #1)

- [x] Core project structure with proper Python packaging
- [x] PDF metadata removal using PyPDF2
- [x] DOCX metadata removal with ZIP manipulation
- [x] CLI interface with argparse
- [x] Basic test suite and GitHub Actions CI
- [x] Comprehensive documentation

## Version 0.2.0 (Image Support)

**Target**: March 2026
**Priority**: High

### Features
- [ ] JPEG EXIF metadata removal
- [ ] PNG metadata (tEXt, iTXt chunks) removal
- [ ] WebP metadata support
- [ ] HEIC/HEIF metadata support (if feasible)
- [ ] Image format auto-detection
- [ ] Preserve image quality options

### Technical Tasks
- [ ] Add Pillow dependency
- [ ] Create ImageHandler base class
- [ ] Implement format-specific handlers
- [ ] Add test fixtures for each image format
- [ ] Update documentation with image examples

## Version 0.3.0 (Enhanced CLI & Batch Processing)

**Target**: April 2026
**Priority**: High

### Features
- [ ] Recursive directory processing (`--recursive`, `-r`)
- [ ] Glob pattern support
- [ ] In-place editing with confirmation (`--in-place`)
- [ ] Backup creation option (`--backup`)
- [ ] Dry-run mode (`--dry-run`)
- [ ] Progress bar for batch operations
- [ ] Summary statistics output
- [ ] Parallel processing for large batches

### CLI Options
```bash
metastripper --recursive ~/Documents/ --backup
metastripper *.pdf --in-place --dry-run
metastripper images/ -r --verbose --parallel
```

## Version 0.4.0 (Selective Metadata Control)

**Target**: May 2026
**Priority**: Medium

### Features
- [ ] Selective field preservation (`--keep author,title`)
- [ ] Selective field removal (`--remove gps,dates`)
- [ ] Metadata profiles (presets for common use cases)
- [ ] Before/after metadata comparison (`--verify`)
- [ ] JSON output for scripting (`--json`)
- [ ] Metadata export to file (`--export metadata.json`)

### Use Cases
```bash
# Keep author but remove everything else
metastripper document.pdf --keep author

# Only remove GPS and timestamps
metastripper photo.jpg --remove gps,dates

# Privacy profile (remove all identifying info)
metastripper file.pdf --profile privacy
```

## Version 0.5.0 (Additional Document Formats)

**Target**: June 2026
**Priority**: Medium

### LibreOffice/OpenDocument Formats
- [ ] ODT (text documents)
- [ ] ODS (spreadsheets)
- [ ] ODP (presentations)
- [ ] Use ZIP manipulation similar to DOCX

### Microsoft Office Formats
- [ ] XLSX (Excel spreadsheets)
- [ ] PPTX (PowerPoint presentations)
- [ ] DOC (legacy Word format - via external tool)

### Other Formats
- [ ] RTF (Rich Text Format)
- [ ] Markdown (YAML frontmatter)
- [ ] Plain text files with metadata comments

## Version 1.0.0 (Production Ready)

**Target**: July 2026
**Priority**: High

### Quality & Stability
- [ ] Comprehensive test coverage (>90%)
- [ ] Performance benchmarks
- [ ] Security audit
- [ ] Cross-platform testing (Linux, macOS, Windows)
- [ ] Memory efficiency for large files
- [ ] Error handling review

### Distribution
- [ ] Publish to PyPI
- [ ] Create Homebrew formula for macOS
- [ ] Package as RPM for Fedora/RHEL
- [ ] Package as DEB for Debian/Ubuntu
- [ ] Snap package for universal Linux
- [ ] Documentation website

### Documentation
- [ ] Man page (`man metastripper`)
- [ ] User guide with examples
- [ ] API documentation for library usage
- [ ] Security best practices guide
- [ ] Format-specific notes

## Version 1.1.0+ (Future Features)

### Advanced Features
- [ ] Audio file metadata (MP3, FLAC, OGG, M4A)
- [ ] Video file metadata (MP4, MOV, AVI)
- [ ] Archive metadata (ZIP, TAR, 7Z)
- [ ] E-book formats (EPUB, MOBI)
- [ ] Archive old metadata before stripping

### Integration & Automation
- [ ] File manager integration (context menu)
  - Nautilus (GNOME)
  - Finder (macOS)
  - Dolphin (KDE)
- [ ] Watch folder mode (daemon)
- [ ] Web service wrapper for teams
- [ ] Python library API improvements
- [ ] Plugin system for custom handlers

### GUI Options (Low Priority)
- [ ] Evaluate need for GUI
- [ ] Simple GTK app for Linux
- [ ] macOS native app
- [ ] Web-based interface option

### Privacy Enhancements
- [ ] Steganography detection warnings
- [ ] File fingerprinting analysis
- [ ] Timestamp normalization
- [ ] Cryptographic verification of stripping
- [ ] Metadata leak detection

## Platform-Specific Goals

### Fedora Linux
- [ ] Submit to Fedora package repositories
- [ ] DNF install support (`dnf install meta-stripper`)
- [ ] RPM with proper dependencies
- [ ] SELinux policy compatibility

### macOS
- [ ] Homebrew tap or core formula
- [ ] Code signing for distributed binaries
- [ ] macOS extended attributes handling
- [ ] Finder Quick Action integration

### Windows (Future)
- [ ] Windows installer (MSI)
- [ ] PowerShell module
- [ ] Windows Explorer context menu
- [ ] File associations

## Community & Ecosystem

- [ ] Create discussion forum/Discord
- [ ] Contribution guidelines refinement
- [ ] Regular release schedule
- [ ] Security vulnerability reporting process
- [ ] Benchmark comparisons with MAT2, ExifTool
- [ ] Blog posts / tutorials
- [ ] Conference talk submissions

## Non-Goals

**Things we explicitly won't do:**
- Full document anonymization (out of scope)
- Steganography removal (too complex)
- Watermark removal (legal concerns)
- Cloud service integration (privacy conflict)
- Telemetry or analytics (privacy-focused tool)

## Contributing to the Roadmap

Have suggestions? Open an issue or discussion! We prioritize features based on:
1. User demand and use cases
2. Technical feasibility
3. Maintenance burden
4. Privacy/security impact
5. Cross-platform compatibility

## Timeline Disclaimer

Timelines are estimates and may shift based on:
- Contributor availability
- Technical challenges
- Community feedback
- Security considerations

Last Updated: February 2026
