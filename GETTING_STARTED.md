# FeatEx Package Template - Getting Started

Congratulations! You now have a complete Python package template for **FeatEx**, a feature engineering library for point-in-time datasets.

## 📁 What Was Created

### Core Package Structure
- **`featex/`** - Main package directory
  - `__init__.py` - Package initialization and public API
  - `pit.py` - Point-in-Time dataset builder
  - `features.py` - Feature aggregation utilities
  - `utils.py` - Helper functions
  - `py.typed` - Type checking support marker

### Configuration Files
- **`pyproject.toml`** - Modern Python project configuration (all dependencies defined here)
- **`MANIFEST.in`** - Package data manifest
- **`pytest.ini`** - Pytest configuration
- **`.pre-commit-config.yaml`** - Pre-commit hooks configuration
- **`.python-version`** - Python version for uv (3.14)

### Documentation
- **`README.md`** - Project overview and quick start
- **`docs/`** - Sphinx documentation
  - `conf.py` - Sphinx configuration
  - `index.rst` - Documentation index
  - `quickstart.rst` - Quick start guide
  - `api_reference.rst` - API documentation
  - `guides/` - Detailed guides
    - `pit_datasets.rst` - Point-in-time concepts
    - `feature_engineering.rst` - Feature engineering patterns

### Project Files
- **`CONTRIBUTING.md`** - Contribution guidelines
- **`CHANGELOG.md`** - Version history template
- **`LICENSE`** - MIT License
- **`.gitignore`** - Git ignore patterns
- **`Makefile`** - Development shortcuts
- **`.github/workflows/ci.yml`** - GitHub Actions CI/CD

### Tests
- **`tests/`** - Test directory
  - `test_pit.py` - Point-in-time builder tests
  - `test_features.py` - Feature aggregator tests

### Examples
- **`examples/`** - Example scripts
  - `basic_workflow.py` - Complete workflow examples
  - `README.md` - Examples guide

## 🚀 Next Steps

### 0. Install UV (Recommended)

[uv](https://docs.astral.sh/uv/) is a fast, reliable Python package manager. Install it:

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or with Homebrew
brew install uv

# Verify installation
uv --version
```

### 1. Update Metadata
Update these files with your information:

```bash
# Update author and URLs in:
- pyproject.toml
- README.md
- docs/conf.py
```

Replace:
- `Your Name` → Your name
- `your.email@example.com` → Your email
- `yourusername` → Vinushan

### 2. Initialize Git Repository
```bash
cd /Users/vinushan/Documents/Projects/featex
git init
git add .
git commit -m "Initial commit: FeatEx package template"
```

### 3. Set Up Development Environment

Using [uv](https://docs.astral.sh/uv/) (recommended):
```bash
cd /Users/vinushan/Documents/Projects/featex

# Creates virtual environment and installs all dependencies
uv sync

# Run commands with uv
uv run pytest
uv run make test
```

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install development dependencies with UV
uv pip install -e ".[dev,docs]"

# Set up pre-commit hooks (optional)
uv run pre-commit install
```

### 4. Verify Setup
```bash
# Run tests
make test

# Check code quality
make lint

# Format code
make format

# Build documentation
make docs
```

## 📚 Development Commands

Use the Makefile for common tasks (automatically uses uv):

```bash
make help                # Show all available commands
make install            # Install package with uv
make install-dev        # Install with dev dependencies
make test               # Run tests
make test-cov          # Run tests with coverage
make lint              # Lint code
make format            # Format code
make type-check        # Check types
make docs              # Build documentation
make clean             # Clean build artifacts
```

Or run commands directly with uv:

```bash
uv sync                                    # Install all dependencies
uv run pytest                              # Run tests
uv run black featex tests                  # Format code
uv run isort featex tests                  # Sort imports
uv run flake8 featex tests                 # Lint
uv run mypy featex --ignore-missing-imports # Type check
```

## 🏗️ Project Structure Overview

```
featex/
├── featex/                    # Main package
│   ├── __init__.py           # Public API
│   ├── pit.py                # Point-in-time datasets
│   ├── features.py           # Feature aggregation
│   └── utils.py              # Utilities
├── tests/                     # Test suite
│   ├── test_pit.py
│   └── test_features.py
├── examples/                  # Usage examples
│   └── basic_workflow.py
├── docs/                      # Documentation
│   ├── conf.py
│   ├── quickstart.rst
│   └── guides/
├── .github/workflows/         # CI/CD
│   └── ci.yml
├── pyproject.toml            # Project config
├── README.md                 # Overview
├── CONTRIBUTING.md           # Contribution guide
├── LICENSE                   # MIT License
└── Makefile                  # Development tasks
```

## 💡 Key Files to Understand

### `pyproject.toml`
Modern Python project configuration. Define dependencies, metadata, and tool settings here.

### `README.md`
First impression for users. Update with your specific use cases and examples.

### `pyproject.toml`
- **pyproject.toml**: Recommended modern approach (PEP 518)

Use pyproject.toml for new projects.

## 🔧 Common Tasks

### Adding Dependencies
1. Update `pyproject.toml`
2. Run `uv pip install -e "[.dev]"`

### Adding New Modules
1. Create new file in `featex/`
2. Add to `featex/__init__.py` imports
3. Add corresponding tests in `tests/`

### Publishing to PyPI
```bash
# Install build tools
uv pip install build twine

# Build distributions
python -m build

# Upload to PyPI
twine upload dist/*
```

## 📖 Documentation

Generate and view documentation:

```bash
make docs
open docs/_build/html/index.html
```

Or manually:
```bash
sphinx-build -b html docs/ docs/_build/html
```

## ✅ Pre-Commit Hooks (Optional)

Set up automatic code quality checks:

```bash
uv pip install pre-commit
uv run pre-commit install

# Test pre-commit locally
uv run pre-commit run --all-files
```

## 🐛 Testing

Run tests with pytest:

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_pit.py

# Run with coverage
pytest --cov=featex --cov-report=html

# Run in verbose mode
pytest -v
```

## 🎯 Now You're Ready!

1. ✅ Package structure created
2. ✅ Documentation template ready
3. ✅ Tests scaffold in place
4. ✅ CI/CD workflow configured
5. ✅ Examples provided

Start building! 🎉

---

## Need Help?

- See `README.md` for project overview
- Check `CONTRIBUTING.md` for contribution guidelines
- Review `docs/quickstart.rst` for usage examples
- Run `make help` for available commands
