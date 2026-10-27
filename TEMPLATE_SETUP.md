# Set up a project from this template

Use this checklist when creating a repository. The README describes installation
and usage for the resulting package.

## Identity and installation

1. Copy the files without `.git`, `.venv`, caches, or generated artifacts, or use
   GitHub's template feature if it is enabled.
2. Set the distribution name, description, authors, and version in `pyproject.toml`.
   Rename `src/project_name` and update imports in tests, the README, documentation,
   `scripts/check_distribution.py`, and notebooks where present. Distribution names
   and Python import names may differ.
3. Replace `greet` and its tests with the project's public API and a runnable
   example. Update the wheel installation check to exercise that API.
4. Run `uv lock`, then the setup and checks in `CONTRIBUTING.md`.
   `uv build` creates a wheel and source distribution; `twine check` validates their
   metadata. `MANIFEST.in` includes the scripts needed by the source distribution's
   tests. The wheel check installs the package in a fresh environment outside the
   checkout. Its `--no-deps` installation suits the dependency-free starter; install
   runtime dependencies in that environment when the package needs them.
5. Replace `YOUR_PACKAGE_NAME` with the published distribution name. For local
   installation from a checkout, use `python -m pip install .`.

## Public GitHub page

- Set the README title, description, features, and quickstart.
- The commented badge block contains paper/arXiv, Hugging Face, PyPI, download,
  documentation, license, testing, and Codecov links. Replace the placeholders and
  enable the links that apply to the project and have working destinations.
- Issue forms use no predefined labels or assignments. Create any required labels
  before adding them to the forms.

## Ownership, license, and security

- Choose a license, fill `LICENSE`, and update package metadata and the README.
- Set supported releases, a monitored private reporting channel, and response
  expectations in `SECURITY.md`. Test the reporting channel.
- Dependabot checks `uv` dependencies and GitHub Actions weekly and proposes
  updates through pull requests. Review those changes and keep `pyproject.toml`
  and `uv.lock` consistent.
- Configure branch protection, required checks, scanning, visibility, and service
  permissions in the repository settings according to the project's requirements.
  These settings are separate from the files in this template.
- When configuring required checks, use the actual check names reported by GitHub.
  The `testing` workflow's job is named `checks`.

## Documentation and coverage

Sphinx builds the documentation locally and in `testing`. Update `docs/conf.py`,
the API reference, and the user pages for the project. Documentation deployment
is disabled.

Line and branch coverage measures the package and its own scripts. Update the
source path in `[tool.coverage.run]` when renaming the package. Coverage reports
are informational; no percentage gate is configured.

`testing` prints coverage and saves XML/HTML reports as GitHub artifacts.
The Codecov upload runs when the repository Actions variable `CODECOV_ENABLED`
is `true`. Configure Codecov and any required `CODECOV_TOKEN` secret before
enabling it. See `docs/coverage.md` for setup and verification.

## Publishing

Publishing is disabled. `.github/workflow-templates/publish.yml.example` contains
inactive build and publish jobs. See `docs/publishing.md` for its configuration.

## Final check

Find remaining placeholders:

```bash
rg -n 'TODO|YOUR_PACKAGE_NAME|DISTRIBUTION_NAME|OWNER|REPOSITORY|ARXIV_ID|LICENSE_ID|project_name' . .github
```

Run the checks from `CONTRIBUTING.md` in a fresh checkout. Check the rendered README,
issue forms, PR template, and a `testing` run on GitHub.
