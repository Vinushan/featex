# Contributing to FeatEx

Thank you for your interest in contributing to FeatEx! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and constructive in all interactions.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/Vinushan/featex.git
   cd featex
   ```
3. **Set up development environment** using [uv](https://docs.astral.sh/uv/):
   ```bash
   uv sync
   ```
   
   If you need an editable install with UV:
   ```bash
   uv pip install -e .
   uv pip install -e ".[dev,docs]"
   ```

## Development Workflow

### Creating a Feature Branch

```bash
git checkout -b feature/my-feature
```

Branch naming conventions:
- `feature/` for new features
- `fix/` for bug fixes
- `docs/` for documentation
- `refactor/` for code refactoring

### Writing Code

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use type hints for better code clarity
- Write docstrings for all public functions and classes
- Keep functions focused and maintainable

### Code Quality

Run these before committing:

```bash
# Format code
black .

# Sort imports
isort .

# Lint
flake8

# Type checking
mypy

# Run tests
pytest
```

### Testing

- Write tests for all new features
- Ensure existing tests pass
- Aim for >80% code coverage

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=featex --cov-report=html
```

## Documentation

- Update docstrings in code
- Update README.md if adding major features
- Add examples in the `examples/` directory for new features
- Build docs locally to verify: `sphinx-build -b html docs/ docs/_build/`

## Committing Changes

Write clear, descriptive commit messages:

```bash
git commit -m "Add point-in-time dataset builder"
```

Good commit message format:
- Imperative mood ("Add feature" not "Added feature")
- Reference issues if relevant: "Fix #123"
- Keep first line under 72 characters
- Add detailed description after blank line if needed

## Submitting a Pull Request

1. **Push to your fork**:
   ```bash
   git push origin feature/my-feature
   ```

2. **Create a Pull Request** on GitHub with:
   - Clear title describing the change
   - Description of what changed and why
   - Reference to related issues (if any)
   - Screenshots/examples (if applicable)

3. **Respond to feedback** and make requested changes

4. **Wait for CI checks** to pass and for maintainer review

## Reporting Issues

- Use GitHub Issues to report bugs or suggest features
- Check existing issues first to avoid duplicates
- Include:
  - Clear description of the issue
  - Steps to reproduce (for bugs)
  - Expected vs actual behavior
  - Python and dependency versions
  - Example code if applicable

## Project Structure

```
featex/
├── featex/              # Main package
│   ├── __init__.py
│   ├── pit.py          # Point-in-time module
│   ├── features.py     # Feature engineering utilities
│   └── utils.py        # Helper functions
├── tests/              # Test files
├── examples/           # Example notebooks and scripts
├── docs/               # Documentation source
└── README.md
```

## Dependencies

- Keep dependencies minimal
- Use widely-supported versions
- Document why each dependency is needed
- Prefer `pyproject.toml` for dependency and packaging configuration

## Questions?

- Open a GitHub Discussion
- Open an issue for bugs or features
- Check existing documentation

---

Thank you for contributing to FeatEx!
