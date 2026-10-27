# Contributing

## Development

Use Python 3.11 and [uv](https://docs.astral.sh/uv/). CI uses uv 0.13.5;
use that version when reproducing its environment. From the repository root:

```bash
uv sync --locked --group dev --extra notebook
uv run --locked pre-commit install
uv run --locked pre-commit run --all-files
uv run --locked pytest --cov --cov-report=term-missing
```

The hook installation enables both file hooks and commit-message checks.
Use `type(scope): summary`, with `chore`, `ci`, `docs`, `feat`, `fix`, or `test`.
For example: `docs(quickstart): clarify local installation`.
If a hook changes files, review the diff, stage it, and retry the commit.

Useful individual checks:

```bash
uv run --locked ruff check .
uv run --locked ruff format --check .
uv run --locked coverage run --append scripts/check_notebooks.py
uv build
uv run --locked twine check dist/*
uv run --locked coverage run --append scripts/check_distribution.py
uv run --locked coverage report
uv run --locked coverage xml
uv run --locked coverage html
```

Configuration lives in `pyproject.toml`, `.pre-commit-config.yaml`, and
`.github/workflows/testing.yml`. Lint checks and automatic corrections
are configured there. Changes to dependencies require `uv lock`; commit both the
manifest and lockfile. See [Template configuration](ASSUMPTIONS.md) for the configuration overview.

The build backend is pinned in `[build-system]`. Update that pin deliberately and
rerun the package checks when upgrading it. `uv.lock` fixes the project development
dependencies; Pre-Commit installs its separately pinned hooks in isolated
environments whose transitive dependencies are resolved independently. These
settings do not promise byte-identical builds across Python versions or platforms.

## Working with notebooks

```bash
uv run --locked --extra notebook jupyter lab
```

Keep customer data and credentials outside the repository. Commit notebooks with
empty code outputs, null execution counts, no attachments, and no saved widget
state. Use Jupyter's clear-output controls and review the diff before committing.
The notebook checker validates structure and these storage rules; it
neither executes the analysis nor detects all sensitive text.

## Pull requests

Keep changes focused. Use the PR template to describe the problem, the resulting
behavior, the commands you ran, and any limitations or unverified behavior.

Run the commands above before opening a PR. Add or update relevant tests when
behavior changes.

Report suspected security vulnerabilities through [SECURITY.md](SECURITY.md).
Do not include secrets, private data, or sensitive logs in issues or pull requests.

## Documentation

```bash
uv sync --locked --group dev --group docs
uv run --locked --group docs sphinx-build -b html docs docs/_build/html
python -m http.server --directory docs/_build/html 8000
```

Open http://localhost:8000. Edit user-facing pages under `docs/`; public API
reference content comes from package docstrings. Sphinx builds the site; MyST supports Markdown pages.
No documentation deployment is enabled.

## Coverage

Line and branch coverage includes the package and own scripts, with no percentage
gate. See [Coverage](docs/coverage.md) for interpretation and the Codecov
opt-in upload integration. Ordinary `pytest` without `--cov` still runs tests without measurement.
See [Template setup](TEMPLATE_SETUP.md) when adapting the repository.
