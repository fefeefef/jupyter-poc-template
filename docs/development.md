# Development

The repository's `CONTRIBUTING.md` is the contributor guide for humans and agents.
The command blocks below are included from that guide so they stay in sync.

## Environment and tests

```{literalinclude} ../CONTRIBUTING.md
:language: bash
:start-after: ```bash
:end-before: ```
```

## Individual checks

```{literalinclude} ../CONTRIBUTING.md
:language: bash
:start-at: uv run --locked ruff check .
:end-at: uv run --locked coverage html
```

## Build and preview documentation

```{literalinclude} ../CONTRIBUTING.md
:language: bash
:start-at: uv sync --locked --group dev --group docs
:end-at: python -m http.server --directory docs/_build/html 8000
```

Open http://localhost:8000. Documentation builds from package docstrings and is
not deployed. See the coverage and publishing pages for the opt-in integrations.
