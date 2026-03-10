# Requirements Folder

This folder contains the development dependencies for the Rhiza project, organized by purpose.

## Files

- **tests.txt** - Testing dependencies (pytest, pytest-cov, pytest-html)
- **tools.txt** - Development tools (pre-commit, python-dotenv)

## Usage

These requirements files are automatically installed by the `make install` command.

To install specific requirement files manually:

```bash
uv pip install -r .rhiza/requirements/tests.txt
uv pip install -r .rhiza/requirements/tools.txt
```

## CI/CD

GitHub Actions workflows automatically install these requirements as needed.
