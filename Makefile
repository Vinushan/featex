.PHONY: help install install-dev test test-cov lint format type-check docs clean

help:
	@echo "FeatEx Development Commands"
	@echo "==========================="
	@echo ""
	@echo "Setup:"
	@echo "  make install          Install package with uv"
	@echo "  make install-dev      Install package with dev dependencies"
	@echo ""
	@echo "Testing:"
	@echo "  make test             Run tests"
	@echo "  make test-cov         Run tests with coverage report"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint             Run linting checks"
	@echo "  make format           Format code with black and isort"
	@echo "  make type-check       Run type checking with mypy"
	@echo ""
	@echo "Documentation:"
	@echo "  make docs             Build documentation"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean            Remove build artifacts and cache files"

install:
	uv pip install -e .

install-dev:
	uv sync

test:
	uv run pytest -v

test-cov:
	uv run pytest --cov=featex --cov-report=html --cov-report=term-missing

lint:
	uv run flake8 featex tests
	uv run pylint featex

format:
	uv run black featex tests
	uv run isort featex tests

type-check:
	uv run mypy featex --ignore-missing-imports

docs:
	cd docs && uv run sphinx-build -b html . _build/html
	@echo "Documentation built in docs/_build/html/index.html"

clean:
	rm -rf build dist *.egg-info
	rm -rf htmlcov .coverage .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	cd docs && rm -rf _build
