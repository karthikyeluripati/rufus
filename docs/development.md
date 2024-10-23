# Rufus Development Guide

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/rufus
cd rufus
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

## Project Structure

```
rufus/
├── src/             # Source code
├── tests/           # Test files
├── docs/            # Documentation
└── examples/        # Example usage
```

## Code Style

We follow these conventions:
- Black for code formatting
- isort for import sorting
- MyPy for type checking
- Pylint for code quality

Configure pre-commit hooks:
```bash
pre-commit install
```

## Testing

1. Run tests:
```bash
pytest tests/
```

2. Run with coverage:
```bash
pytest --cov=src/rufus tests/
```

3. Run type checking:
```bash
mypy src/rufus
```

## Adding New Features

1. Create a new branch:
```bash
git checkout -b feature/your-feature
```

2. Implement the feature:
   - Add tests in `tests/`
   - Update documentation
   - Follow type hints
   - Add error handling

3. Run tests and linting:
```bash
pytest tests/
black src/
isort src/
mypy src/
```

4. Create pull request

## Building Components

### 1. Crawlers

Create new crawlers by extending `BaseCrawler`:

```python
from rufus.crawler.base import BaseCrawler

class CustomCrawler(BaseCrawler):
    async def crawl(self, url: str, max_depth: int = 3):
        # Implementation
        pass
```

### 2. Extractors

Create new extractors by extending `BaseExtractor`:

```python
from rufus.extractors.base import BaseExtractor

class CustomExtractor(BaseExtractor):
    async def extract(self, content: str):
        # Implementation
        pass
```

## Documentation

1. Add docstrings to all functions:
```python
def function(arg: str) -> str:
    """
    Function description.

    Args:
        arg: Argument description

    Returns:
        Return value description
    """
    pass
```

2. Update API documentation for new endpoints

3. Add examples to `examples/` directory

## Debugging

1. Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

2. Use debugger:
```python
import pdb; pdb.set_trace()
```

## Performance Optimization

1. Profile code:
```python
import cProfile
cProfile.run('function()')
```

2. Memory profiling:
```python
from memory_profiler import profile

@profile
def function():
    pass
```

## Security Considerations

- Validate all inputs
- Use rate limiting
- Handle sensitive data properly
- Follow security best practices