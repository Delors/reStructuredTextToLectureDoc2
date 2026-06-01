# Developer Documentation

This document is intended for developers working on `rst2ld`.

## Requirements

- Python >= 3.13
- See `pyproject.toml` / `requirements.txt` for runtime dependencies.

## Install in Development Mode

```bash
pip install -e ".[test]"
```

This installs the package in editable mode together with the test dependencies.

## Run Tests

```bash
pytest
```

Tests are located in `lddocutils/ldwriter/lddirectives/tests/`.

## Project Structure

- `lddocutils/ldwriter/` — custom Docutils writer (`LDTranslator`) and directive definitions.
- `lddocutils/ldwriter/lddirectives/` — monkey-patched and custom directives.
- `lddocutils/ldwriter/lddirectives/tests/` — pytest test suite.
- `rst2ld.py` — command-line entry point.
