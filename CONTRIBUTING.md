# Contributing to meta-stripper

First off, thanks for taking the time to contribute! 🚀

We welcome contributions from the community to help improve meta-stripper.

## How to Contribute

### Reporting Bugs

If you find a bug or unexpected behavior:
- Check if the issue already exists in [GitHub Issues](https://github.com/KnowOneActual/meta-stripper/issues)
- Provide as much detail as possible:
  - Operating system (Fedora, macOS, etc.)
  - Python version (`python --version`)
  - meta-stripper version (`metastripper --version`)
  - Steps to reproduce
  - Example file if possible (without sensitive data)

### Requesting Features

Have an idea for a new feature or improvement?
- Open a Feature Request issue
- Describe **why** this feature would be useful
- Include potential use cases
- If suggesting a new file format, provide format documentation links

### Submitting Changes (Pull Requests)

1. **Fork the Repository**
   ```bash
   git clone https://github.com/YOUR-USERNAME/meta-stripper.git
   cd meta-stripper
   ```

2. **Set up Development Environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install in development mode with dev dependencies
   pip install -e ".[dev]"
   ```

3. **Create a Feature Branch**
   ```bash
   git checkout -b feature/my-new-feature
   # or
   git checkout -b fix/bug-description
   ```

4. **Make Your Changes**
   - Write clean, documented code
   - Follow existing code style (enforced by Black and Ruff)
   - Add tests for new functionality
   - Update documentation as needed

5. **Run Tests and Linting**
   ```bash
   # Run tests
   pytest tests/ -v
   
   # Check coverage
   pytest tests/ --cov=src/metastripper --cov-report=term-missing
   
   # Format code
   black src/ tests/
   
   # Lint code
   ruff check src/ tests/
   ```

6. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat: add image metadata support for JPEG"
   ```
   
   Use conventional commit messages:
   - `feat:` - New features
   - `fix:` - Bug fixes
   - `docs:` - Documentation changes
   - `test:` - Test additions/changes
   - `refactor:` - Code refactoring
   - `chore:` - Maintenance tasks

7. **Push and Create Pull Request**
   ```bash
   git push origin feature/my-new-feature
   ```
   Then open a Pull Request against the `main` branch on GitHub.

## Development Guidelines

### Code Style

- **Python Version**: Target Python 3.8+ for broad compatibility
- **Formatting**: Use [Black](https://black.readthedocs.io/) (100 char line length)
- **Linting**: Use [Ruff](https://docs.astral.sh/ruff/) for fast linting
- **Type Hints**: Use type hints for function signatures
- **Docstrings**: Use Google-style docstrings for all public functions

### Adding New File Format Handlers

1. Create a new handler in `src/metastripper/handlers/`:
   ```python
   from pathlib import Path
   from typing import Optional, Dict, Any
   from .base import BaseHandler
   
   class NewFormatHandler(BaseHandler):
       def display_metadata(self, filepath: Path) -> Optional[Dict[str, Any]]:
           # Implementation
           pass
       
       def strip_metadata(self, input_path: Path, output_path: Path) -> None:
           # Implementation
           pass
   ```

2. Register the handler in `src/metastripper/handlers/__init__.py`:
   ```python
   HANDLER_MAP = {
       '.pdf': PDFHandler,
       '.docx': DOCXHandler,
       '.jpg': NewFormatHandler,  # Add here
   }
   ```

3. Add tests in `tests/test_handlers.py`
4. Update README.md supported formats list

### Testing

- Write tests for all new functionality
- Aim for >80% code coverage
- Use pytest fixtures for test files
- Test edge cases: corrupted files, empty files, large files

### Documentation

When adding features, update:
- README.md - Usage examples and supported formats
- CHANGELOG.md - Document changes
- Docstrings - Keep code documentation current

## Project Structure

```
meta-stripper/
├── src/
│   └── metastripper/
│       ├── __init__.py          # Package exports
│       ├── __main__.py          # python -m entry point
│       ├── cli.py               # Command-line interface
│       ├── core.py              # Core orchestration
│       └── handlers/
│           ├── __init__.py      # Handler registration
│           ├── base.py          # Abstract base class
│           ├── pdf.py           # PDF handler
│           └── docx.py          # DOCX handler
├── tests/                       # Test suite
├── pyproject.toml              # Project config
└── README.md
```

## Questions?

Feel free to open a discussion or issue if you have questions about contributing.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
