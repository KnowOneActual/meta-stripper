# Security Policy

## Supported Versions

We release patches for security vulnerabilities for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability in meta-stripper, please report it responsibly.

### How to Report

**Please do NOT report security vulnerabilities through public GitHub issues.**

Instead, please report security issues by:

1. Opening a [Security Advisory](https://github.com/KnowOneActual/meta-stripper/security/advisories/new) on GitHub (preferred)
2. Emailing the maintainers (if listed in package metadata)

### What to Include

Please include as much of the following information as possible:

- Type of vulnerability (e.g., buffer overflow, SQL injection, XSS, path traversal)
- Full paths of source file(s) related to the vulnerability
- Location of the affected source code (tag/branch/commit or direct URL)
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the vulnerability (what an attacker could do)
- Any suggested fixes or mitigations

### Response Timeline

We will:

- Acknowledge receipt of your vulnerability report within **48 hours**
- Provide an initial assessment within **7 days**
- Work to fix confirmed vulnerabilities as quickly as possible
- Keep you informed of progress throughout the process
- Credit you in the security advisory (unless you prefer to remain anonymous)

## Security Considerations for Users

### What This Tool Does

meta-stripper removes **standard metadata fields** from documents. It:

- ✅ Removes author, title, creation dates, and similar metadata
- ✅ Works on local files only (no network access)
- ✅ Creates new files, never modifies originals by default

### What This Tool Does NOT Do

meta-stripper does **not** provide complete anonymization:

- ❌ Does NOT remove steganographic data
- ❌ Does NOT strip watermarks or visual identifiers
- ❌ Does NOT guarantee complete anonymization
- ❌ Does NOT remove tracking pixels or embedded objects
- ❌ Does NOT sanitize document content

### Best Practices

For maximum privacy:

1. **Verify metadata removal**: Use `--show` before and after stripping
2. **Combine tools**: Use meta-stripper alongside other sanitization tools
3. **Review content**: Manually review document content for identifying information
4. **Test first**: Always test on non-sensitive files first
5. **Keep backups**: Ensure you have backups before processing important files
6. **Update regularly**: Keep meta-stripper updated for latest security fixes

### File Handling

meta-stripper:

- Never sends files over the network
- Never uploads data to external services
- Operates entirely on local files
- Does not create log files containing file content
- Does not retain processed files in memory longer than necessary

## Known Limitations

### PDF Files

- Embedded objects may retain metadata
- Encrypted PDFs are not supported
- Some PDF features may be lost (rare)

### DOCX Files

- Revision history is preserved in document structure
- Comments and tracked changes are NOT removed
- Embedded files retain their metadata

### General

- File timestamps on filesystem are not modified
- File fingerprinting may still be possible
- Very large files may consume significant memory

## Security Updates

Security updates will be:

- Released as patch versions (e.g., 0.1.1)
- Documented in CHANGELOG.md
- Announced via GitHub releases
- Tagged with "security" label

## Dependencies

We regularly review and update dependencies:

- PyPDF2: PDF parsing and manipulation
- Standard library only otherwise

Dependencies are kept minimal to reduce attack surface.

## Disclosure Policy

We follow coordinated vulnerability disclosure:

1. Security researcher reports vulnerability
2. We confirm and develop a fix
3. We release the fix
4. We publicly disclose the vulnerability details

We aim to release fixes before public disclosure.

## Bug Bounty

We currently do not offer a bug bounty program, but we deeply appreciate responsible disclosure and will credit researchers in security advisories.

---

**Last Updated**: February 2026
