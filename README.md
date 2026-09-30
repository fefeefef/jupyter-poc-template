# TODO: Customer PoC project name

TODO: Describe the PoC without including customer or product-confidential details.

## Use this template

Copy this directory as the starting point for a new repository. Complete the TODOs below, then run uv lock to refresh uv.lock after changing project metadata or dependencies. Python 3.11, uv with a committed lockfile, and the Ruff rules are starting choices for this template; align the Python requirement, Ruff target, CI version, and dependency workflow with the actual PoC. Follow existing organization rules when they prescribe different settings.

## Before first use

- [ ] TODO: Replace the project name in this README and pyproject.toml.
- [ ] TODO: Rename src/project_name.
- [ ] TODO: Replace the description with an approved public-safe summary.
- [ ] TODO: Choose a license and add its approved license file or metadata.
- [ ] TODO: Name the responsible team or maintainers.
- [ ] Check current organization and customer rules before adopting this optional template.

## Local setup

Install uv, then run:

    uv sync --locked --group dev --extra notebook
    uv run --locked --extra notebook jupyter lab
    uv run --locked python scripts/check_notebooks.py
    uv run --locked pytest
    uv run --locked ruff check .
    uv run --locked ruff format --check .

After initializing Git, enable the local hooks:

    uv run --locked pre-commit install
    uv run --locked pre-commit run --all-files

Keep only source code and safe, empty-output notebooks in Git. This empty-output rule is a customer-PoC safeguard chosen for this template, not a verified organization-wide rule. The notebook check validates notebook structure and rejects saved code outputs, execution counts, attachments, and widget state. It does not run cells or detect all confidential text. Keep customer data and credentials outside the repository and review every change before committing. If the project needs approved, synthetic test fixtures, narrow the relevant .gitignore rules explicitly so those fixtures can be tracked without admitting customer data.

CI performs static quality checks, tests, and all Pre-Commit hooks on pushes and pull requests. The hooks check common file hygiene and private-key patterns. Neither workflow runs notebook cells, deploys, or publishes.

See ASSUMPTIONS.md for decisions and limits inherited from the template proposal.
