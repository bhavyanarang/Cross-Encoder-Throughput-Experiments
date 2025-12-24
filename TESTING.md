# Testing Guide

## Overview

This project includes automated testing and CI/CD integration for code quality and functionality.

## Pre-commit Hooks

Pre-commit hooks automatically run linting and formatting before each commit:

```bash
# Install pre-commit hooks (already done)
pre-commit install

# Run manually on all files
pre-commit run --all-files

# Run on staged files only (automatic on commit)
pre-commit run
```

### What Pre-commit Checks

- **Trailing whitespace**: Removes trailing whitespace
- **End of file**: Ensures files end with newline
- **YAML/JSON/TOML**: Validates configuration files
- **Ruff linting**: Python code linting with auto-fix
- **Ruff formatting**: Python code formatting

## Running Tests Locally

```bash
# Activate virtual environment
source venv/bin/activate

# Install test dependencies
pip install -r requirements.txt

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=ml_inference_server --cov-report=term --cov-report=html

# Run specific test file
pytest tests/test_backends.py -v

# Run specific test
pytest tests/test_backends.py::TestBackends::test_backend_creation -v
```

## CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/ci.yml`) automatically runs:

1. **Lint Job**: Runs pre-commit hooks on all files
2. **Test Job**: Runs pytest with coverage reporting

### Triggered On

- Push to `main`, `master`, or `develop` branches
- Pull requests to `main`, `master`, or `develop` branches

## Test Structure

```
tests/
├── __init__.py          # Test package initialization
├── conftest.py          # Pytest fixtures and configuration
├── test_backends.py     # Backend implementation tests
├── test_config.py       # Configuration loading tests
└── README.md            # Test documentation
```

## Adding New Tests

1. Create test files following the pattern `test_*.py`
2. Use descriptive test class and method names
3. Use fixtures from `conftest.py` when possible
4. Keep tests fast and isolated (use mocks for external services)

Example:

```python
import pytest
from ml_inference_server.backends import create_backend

class TestMyFeature:
    def test_feature_works(self):
        # Test implementation
        assert True
```

## Known Issues

### Protobuf Version Compatibility

If you encounter protobuf import errors when running experiments, you may need to regenerate the protobuf files:

```bash
cd ml_inference_server/proto
python -m grpc_tools.protoc --python_out=. --grpc_python_out=. inference.proto
```

Or update protobuf:

```bash
pip install --upgrade protobuf grpcio-tools
```

## Coverage Goals

- Aim for >80% code coverage
- Focus on critical paths (backends, scheduling, configuration)
- Integration tests for end-to-end workflows
