# FeatEx - Feature Engineering for Point-in-Time Datasets

[![Python Version](https://img.shields.io/badge/python-3.14%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![CI/CD](https://github.com/yourusername/featex/workflows/CI/badge.svg)](https://github.com/yourusername/featex/actions)

**FeatEx** is a Python library designed to simplify feature engineering and the creation of point-in-time (PIT) datasets for machine learning workflows. It provides tools for temporal feature engineering, data aggregation, and generating consistent training/evaluation datasets that respect time boundaries.

## Features

- **Point-in-Time Datasets**: Build historically accurate datasets that avoid data leakage
- **Temporal Feature Engineering**: Create features based on historical time windows
- **Data Aggregation**: Efficient aggregation of features at different time granularities
- **Flexible API**: Work seamlessly with pandas DataFrames
- **Performance Optimized**: Designed for handling large-scale datasets

## Installation

### From PyPI (coming soon)

```bash
uv pip install featex
```

### From source (development)

We recommend using [uv](https://docs.astral.sh/uv/) for fast, reliable development setup:

```bash
git clone https://github.com/yourusername/featex.git
cd featex
uv sync  # Creates virtual environment and installs dependencies
uv run make test  # Verify installation
```

For editable development installs with UV:

```bash
uv pip install -e ".[dev]"
```

## Quick Start

```python
import pandas as pd
from featex.pit import PointInTimeBuilder

# Create sample data
data = pd.DataFrame({
    'user_id': [1, 1, 1, 2, 2],
    'timestamp': pd.date_range('2023-01-01', periods=5, freq='D'),
    'amount': [100, 150, 200, 50, 75]
})

# Build point-in-time dataset
pit_builder = PointInTimeBuilder(
    entity_col='user_id',
    timestamp_col='timestamp',
    observation_date='2023-01-03'
)

pit_dataset = pit_builder.transform(data)
print(pit_dataset)
```

## Documentation

Full documentation is available at [featex.readthedocs.io](https://featex.readthedocs.io) (coming soon).

## Key Concepts

### Point-in-Time Datasets

A point-in-time dataset is a snapshot of features at a specific moment in time, using only data that would have been available at that moment. This is crucial for preventing data leakage in machine learning models.

### Example Use Cases

- **Credit Risk**: Build features from customer transaction history up to a loan application date
- **E-commerce**: Create purchase prediction features from historical buying patterns
- **Healthcare**: Generate patient health profiles using only past medical records
- **Fraud Detection**: Build fraud features from transaction history before a specific date

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Make your changes
4. Add tests for new functionality
5. Run tests (`pytest`)
6. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## Development

### Setup Development Environment

**Prerequisites**: Install [uv](https://docs.astral.sh/uv/install/)

**Prerequisites**: Install [uv](https://docs.astral.sh/uv/install/)

```bash
# Create virtual environment and install dependencies
uv sync

# Run tests
uv run pytest              # Run all tests
uv run pytest -v           # Verbose output
uv run pytest --cov        # With coverage report
```

### Code Quality

```bash
uv run black .             # Format code
uv run isort .             # Sort imports
uv run flake8              # Lint
uv run mypy                # Type checking
```

### Documentation

```bash
uv run sphinx-build -b html docs/ docs/_build/html
```

### Using Make

```bash
make help                  # Show all commands
make test                  # Run tests
make lint                  # Lint code
make format                # Format code
make docs                  # Build documentation
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and updates.

## Citation

If you use FeatEx in your research, please cite it as:

```bibtex
@software{featex2024,
  author = {Your Name},
  title = {FeatEx: Feature Engineering for Point-in-Time Datasets},
  year = {2024},
  url = {https://github.com/yourusername/featex}
}
```

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/featex/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/featex/discussions)

## Roadmap

- [ ] Support for multiple data backends (SQL, Parquet)
- [ ] Distributed computing support (Dask, Spark)
- [ ] Advanced time-based aggregations
- [ ] Feature store integration
- [ ] Web UI for feature management

---

**Note**: FeatEx is currently in early alpha. The API may change as the project evolves. Feedback and contributions are highly welcome!
