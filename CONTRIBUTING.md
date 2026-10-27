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
`.github/workflows/testing.yml`. Existing lint selections and automatic corrections
remain defined there. Changes to dependencies require `uv lock`; commit both the
manifest and lockfile. See [Template assumptions](ASSUMPTIONS.md) for inherited choices.

## Working with notebooks

```bash
uv run --locked --extra notebook jupyter lab
```

Keep customer data and credentials outside the repository. Commit notebooks with
empty code outputs, null execution counts, no attachments, and no saved widget
state. Use Jupyter's clear-output controls and review the diff before committing.
The existing notebook checker validates structure and these storage rules; it
neither executes the analysis nor detects all sensitive text.

## Pull requests

Keep changes focused. Use the PR template to describe the problem, the resulting
behavior, the commands you actually ran, and anything not verified. Agents should
report the same evidence and clearly identify unresolved decisions.

Run the commands above before opening a PR. Add or update relevant tests when
behavior changes. Do not invent a coverage threshold, CLA obligation, changelog
rule, or review response deadline. Those policies belong to the project owners.

Report suspected security vulnerabilities through [SECURITY.md](SECURITY.md).
Do not include secrets, private data, or sensitive logs in issues or pull requests.

## Documentation

```bash
uv sync --locked --group dev --group docs
uv run --locked --group docs sphinx-build -b html docs docs/_build/html
python -m http.server --directory docs/_build/html 8000
```

Open http://localhost:8000. Edit user-facing pages under `docs/`; public API
reference content comes from package docstrings. Sphinx follows the explicit tool
named in the feedback; MyST lets the coverage and publishing notes remain Markdown.
No documentation deployment is enabled.

## Coverage

Line and branch coverage includes the package and own scripts, with no percentage
gate. See [Coverage](docs/coverage.md) for interpretation and the Codecov
opt-in upload integration. Ordinary `pytest` without `--cov` still runs tests without measurement.
See [Template setup](TEMPLATE_SETUP.md) when adapting the repository.
