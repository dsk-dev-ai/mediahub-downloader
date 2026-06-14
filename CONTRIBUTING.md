# Contributing to MediaHub Downloader

Thank you for considering contributing to MediaHub Downloader! We welcome contributions from the community.

## How to Contribute

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Make your changes
4. Ensure your code follows our coding standards
5. Add tests for your changes
6. Run the test suite to ensure everything passes
7. Submit a pull request

## Coding Standards

- Follow PEP 8 for Python code style
- Use type hints for all function parameters and return values
- Write clear, descriptive docstrings for all public methods
- Keep functions focused and small (ideally under 50 lines)
- Use meaningful variable and function names
- Comment complex logic, but avoid obvious comments

## Development Setup

1. Clone your fork: `git clone https://github.com/your-username/mediahub-downloader.git`
2. Create a virtual environment: `python3 -m venv .venv`
3. Activate the virtual environment: `source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Install development dependencies: `pip install -r requirements.txt` (includes testing dependencies)

## Running Tests

To run the test suite:

```bash
python -m pytest tests/ -v
```

To run tests with coverage:

```bash
python -m pytest tests/ --cov=app --cov-report=html
```

## Pull Request Process

1. Ensure your code passes all tests
2. Update the README.md if needed for your changes
3. The pull request will be reviewed by maintainers
4. Once approved, your changes will be merged

## Reporting Issues

Please use the GitHub issue tracker to report bugs or suggest features. When reporting a bug, please include:

- Steps to reproduce the issue
- Expected behavior vs actual behavior
- Screenshots if applicable
- Your operating system and Python version

## License

By contributing to MediaHub Downloader, you agree that your contributions will be licensed under the same license as the project.