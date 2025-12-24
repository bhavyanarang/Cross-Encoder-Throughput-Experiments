# Tests

This directory contains tests for the ML Inference Server.

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=ml_inference_server --cov-report=term

# Run specific test file
pytest tests/test_backends.py -v

# Run specific test
pytest tests/test_backends.py::TestBackends::test_backend_creation -v
```

## Test Structure

- `test_backends.py`: Tests for backend implementations
- `test_config.py`: Tests for configuration loading and validation
- `conftest.py`: Pytest fixtures and configuration

## Adding New Tests

When adding new tests:

1. Create test files following the pattern `test_*.py`
2. Use descriptive test class and method names
3. Use fixtures from `conftest.py` when possible
4. Ensure tests are fast and don't require external services (use mocks when needed)

## CI Integration

Tests are automatically run on:
- Every push to main/master/develop branches
- Every pull request

See `.github/workflows/ci.yml` for CI configuration.
