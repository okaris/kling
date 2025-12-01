# Contributing to Kling AI SDK

Thank you for your interest in contributing!

## Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd kling
   ```

2. **Install dependencies**
   ```bash
   # Using Poetry (recommended)
   poetry install

   # Or using pip
   pip install -e ".[dev]"
   ```

3. **Set up authentication**
   ```bash
   export KLING_ACCESS_KEY="ak-your-access-key"
   export KLING_SECRET_KEY="your-secret-key"
   ```

## Code Style

We use:
- **Black** for code formatting
- **Ruff** for linting
- **mypy** for type checking

```bash
# Format code
poetry run black kling/

# Lint
poetry run ruff check kling/

# Type check
poetry run mypy kling/
```

## Project Structure

```
kling/
├── kling/              # Main package
│   ├── api/            # API endpoint implementations
│   ├── models/         # Pydantic models
│   ├── base.py         # Base client
│   ├── client.py       # Main client
│   └── exceptions.py   # Custom exceptions
├── examples/           # Usage examples
└── tests/              # Test suite (to be added)
```

## Adding New Features

### 1. Add Pydantic Models

In `kling/models/`, create models for requests and responses:

```python
from pydantic import BaseModel, Field

class NewFeatureRequest(BaseModel):
    param1: str = Field(..., description="Description")
    param2: Optional[int] = Field(None, description="Optional param")
```

### 2. Create API Module

In `kling/api/`, create a new API class:

```python
from kling.base import BaseAPIClient
from kling.models.common import TaskResponse

class NewFeatureAPI:
    def __init__(self, client: BaseAPIClient):
        self.client = client
        self.endpoint = "/v1/your-endpoint"

    def create(self, **kwargs) -> TaskResponse:
        # Implementation
        pass

    async def create_async(self, **kwargs) -> TaskResponse:
        # Async implementation
        pass
```

### 3. Update Main Client

Add the new API to `KlingClient` in `kling/client.py`:

```python
class KlingClient:
    def __init__(self, ...):
        # ...
        self.new_feature = NewFeatureAPI(self._base_client)
```

### 4. Add Examples

Create an example in `examples/` showing how to use the new feature.

### 5. Update Documentation

Update README.md and QUICKSTART.md with the new feature.

## Testing

```bash
# Run tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=kling --cov-report=html
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linters
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Code Review Guidelines

- Follow existing code style
- Add type hints to all functions
- Include docstrings for public methods
- Update examples if adding new features
- Keep changes focused and atomic

## Questions?

Feel free to open an issue for questions or discussions!
