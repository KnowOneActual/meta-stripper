.PHONY: help install install-dev test test-cov lint format check clean

# Default target
help:
	@echo "meta-stripper development commands:"
	@echo ""
	@echo "  make install      - Install package"
	@echo "  make install-dev  - Install package with dev dependencies"
	@echo "  make test         - Run tests"
	@echo "  make test-cov     - Run tests with coverage report"
	@echo "  make lint         - Run linters (ruff)"
	@echo "  make format       - Format code (black, ruff)"
	@echo "  make check        - Run all checks (format, lint, test)"
	@echo "  make type-check   - Run type checking (mypy)"
	@echo "  make clean        - Remove build artifacts"
	@echo "  make pre-commit   - Install and run pre-commit hooks"
	@echo ""

# Installation
install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

# Testing
test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=src/metastripper --cov-report=term-missing --cov-report=html

test-fast:
	pytest tests/ -v -x  # Stop on first failure

# Linting
lint:
	@echo "Running ruff..."
	ruff check src/ tests/

lint-fix:
	@echo "Running ruff with auto-fix..."
	ruff check src/ tests/ --fix

# Formatting
format:
	@echo "Running black..."
	black src/ tests/
	@echo "Running ruff import sorting..."
	ruff check src/ tests/ --select I --fix

format-check:
	@echo "Checking code format..."
	black --check src/ tests/

# Type checking
type-check:
	@echo "Running mypy..."
	mypy src/

# Combined checks
check: format-check lint test
	@echo "✅ All checks passed!"

# Pre-commit
pre-commit:
	pre-commit install
	pre-commit run --all-files

# Cleaning
clean:
	@echo "Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete

# Development workflow
dev-setup: install-dev pre-commit
	@echo "✅ Development environment ready!"

ci: format-check lint type-check test-cov
	@echo "✅ CI checks passed!"
