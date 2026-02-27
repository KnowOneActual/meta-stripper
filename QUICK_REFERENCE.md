# Quick Reference Guide: Document Metadata Removal

## 🚨 Why This Matters

**Every document you share contains hidden metadata that can expose:**
- Employee names and email addresses
- Internal file paths and network structure
- Software versions (security vulnerability information)
- Edit history and deleted content
- Company organizational details
- Confidential comments and tracked changes

**Bottom line:** Sharing documents without removing metadata is a privacy and security risk.

---

## ⚡ Quick Start

```bash
# Install meta-stripper
git clone https://github.com/KnowOneActual/meta-stripper.git
cd meta-stripper
pip install -e .

# Strip metadata from a file
metastripper document.pdf

# Check metadata before removing
metastripper --show document.pdf
```

---

## 📋 Common Use Cases

### Before Sending to Clients
```bash
metastripper contract.pdf proposal.docx specs.pdf
```

### Before Publishing Online
```bash
metastripper press_release.pdf whitepaper.docx
```

### Check What's Inside First
```bash
metastripper --show sensitive_document.pdf
```

### Specify Output Name
```bash
metastripper internal_report.pdf -o client_report.pdf
```

### Clean an Entire Directory Recursively
```bash
metastripper -r documents/
```

### Overwrite Original Files (In-Place)
```bash
metastripper -i photo.jpg --backup
```

### Keep Only Specific Metadata Fields
```bash
# Only Author and Title will be kept; all other fields removed
metastripper document.pdf --keep Author Title
```

### Remove Only Specific Metadata Fields
```bash
# Only GPS data will be removed; all other fields preserved
metastripper photo.jpg --remove GPS
```

### Preview Changes Before Acting
```bash
# See which files would be processed without any modifications
metastripper -r docs/ --dry-run
```

---

## 🎯 When to Remove Metadata

✅ **ALWAYS remove metadata before:**
- Sending documents to clients or vendors
- Publishing files on your website
- Submitting materials in legal proceedings
- Sharing with external contractors
- Posting to social media or press releases
- Responding to FOIA/public records requests
- Uploading to cloud services
- Email attachments to external parties

❌ **Keep metadata for:**
- Internal documents and collaboration
- Version control and document management
- Audit trails and compliance records
- Documents that never leave your organization

---

## 🔍 What Gets Removed

### PDF Files
- Author, Creator, Producer
- Title, Subject, Keywords
- Creation and modification dates
- Custom metadata fields
- Software version information

### DOCX Files
- Author and company name
- Document template information
- Total editing time
- Revision count
- Manager and category fields
- Custom properties
- Extended properties (application details)

---

## ⚠️ What Does NOT Get Removed

- Visible text and images
- Document formatting and layout
- Embedded fonts and styles
- Watermarks (visible or invisible)
- Steganographic data
- Digital signatures (these will be invalidated)

**Important:** Always review document content separately. Metadata removal doesn't redact visible information.

---

## 🛡️ Security Checklist

Before sharing any document externally:

- [ ] Remove metadata using meta-stripper
- [ ] Review visible content for sensitive information
- [ ] Check file naming for confidential details
- [ ] Verify tracked changes are accepted/rejected
- [ ] Ensure comments are deleted
- [ ] Confirm hidden text is removed
- [ ] Test output file to ensure functionality

---

## 📊 Risk Examples by Industry

| Industry | Risk | Metadata Exposure |
|----------|------|-------------------|
| **Legal** | Client confidentiality | Attorney names, billing hours, edit history |
| **Healthcare** | HIPAA violations | Patient info in author fields, PHI in comments |
| **Media** | Unreleased content | Project names, production schedules, plot details |
| **Finance** | Competitive intel | Client names, deal terms, analyst notes |
| **Government** | FOIA compliance | Policy deliberations, interagency coordination |
| **Technology** | IP protection | Feature roadmaps, source code references |

---

## 🔧 Command Reference

```bash
# Basic usage
metastripper <file>                    # Strip metadata, create new file
metastripper file1.pdf file2.docx      # Process multiple files
metastripper -r <dir>                  # Process directory recursively

# Options
metastripper -o output.pdf input.pdf   # Specify output name
metastripper -i document.pdf           # Clean original file in-place
metastripper -i --backup file.pdf      # Clean in-place, create .bak backup
metastripper --dry-run -r docs/        # Preview processing without acting
metastripper --keep Author file.pdf    # Keep only Author field
metastripper --remove GPS photo.jpg    # Remove only GPS metadata
metastripper --show document.pdf       # Display metadata only
metastripper -v document.pdf           # Verbose output
metastripper --version                 # Show version
metastripper -h                        # Show help
```

---

## 💡 Best Practices

### 1. Make It a Workflow Step
Add metadata removal as a standard step before external sharing

### 2. Keep Original Files
Meta-stripper creates new files automatically. Keep originals for internal use.

### 3. Use Descriptive Output Names
```bash
metastripper internal_v5.pdf -o client_final.pdf
```

### 4. Verify Before Sending
```bash
metastripper --show cleaned_document.pdf
```

### 5. Batch Process Project Folders
```bash
cd project_deliverables/
metastripper *.pdf *.docx
```

### 6. Train Your Team
Ensure everyone understands metadata risks and knows how to use the tool

---

## 🚀 Quick Decision Tree

```
Are you sharing this document externally?
├─ NO  → Keep metadata (internal use only)
└─ YES → Does it contain sensitive work?
    ├─ NO  → Still strip metadata (defense in depth)
    └─ YES → ALWAYS strip metadata
             ↓
             metastripper document.pdf
             ↓
             Verify output
             ↓
             Share cleaned version
```

---

## 📚 Learn More

- **Detailed explanation:** [WHY_METADATA_MATTERS.md](WHY_METADATA_MATTERS.md)
- **Full documentation:** [README.md](README.md)
- **Security policy:** [SECURITY.md](SECURITY.md)
- **Future features:** [ROADMAP.md](ROADMAP.md)

---

## 🆘 Quick Troubleshooting

**Problem:** Command not found  
**Solution:** Run `pip install -e .` from the meta-stripper directory

**Problem:** File not supported  
**Solution:** Currently supports PDF, Word (DOCX), Excel (XLSX), PowerPoint (PPTX), JPEG, PNG, and WebP. See [ROADMAP](ROADMAP.md) for upcoming formats

**Problem:** Need to process many files  
**Solution:** Use wildcards: `metastripper *.pdf` or provide multiple files

**Problem:** Want to verify metadata was removed  
**Solution:** Use `metastripper --show cleaned_file.pdf` to inspect

---

## 💬 Questions?

- Open an issue: [GitHub Issues](https://github.com/KnowOneActual/meta-stripper/issues)
- Start a discussion: [GitHub Discussions](https://github.com/KnowOneActual/meta-stripper/discussions)

---

**Remember:** One metadata leak can compromise privacy, security, and competitive position.  
**Make metadata removal a habit, not an afterthought.**
