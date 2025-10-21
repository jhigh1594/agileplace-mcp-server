# Contributing to AgilePlace MCP Server

Thank you for your interest in contributing to the AgilePlace MCP Server!

## Development Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
3. Set up your environment variables in `.env`
4. Run tests to verify setup:
   ```bash
   pytest
   ```

## Code Style

- Use Black for code formatting: `black src tests`
- Use Ruff for linting: `ruff check src tests`
- Follow PEP 8 guidelines
- Write descriptive docstrings for all functions and classes

## Testing

- Write tests for all new features
- Ensure all tests pass before submitting PR
- Aim for high test coverage
- Use pytest fixtures for reusable test data

## Pull Request Process

1. Create a feature branch from `main`
2. Make your changes with appropriate tests
3. Update documentation if needed
4. Ensure all tests pass and code is formatted
5. Submit a pull request with a clear description

## Reporting Issues

When reporting issues, please include:
- Python version
- AgilePlace MCP Server version
- Steps to reproduce
- Expected vs actual behavior
- Error messages or logs

## Questions?

Feel free to open an issue for questions or discussion.

