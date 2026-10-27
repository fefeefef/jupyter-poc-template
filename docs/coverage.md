# Coverage and Codecov

Line and branch coverage are measured for `src/project_name` and `scripts`.
This scope and reporting-only behavior were explicitly approved by the user.
No minimum percentage, warning threshold, or merge gate is configured.

Line coverage records which executable lines ran. Branch coverage also records
which paths through decisions were taken. A high percentage does not prove the
assertions are meaningful or that all relevant behavior is tested.

From the repository root, start a new measurement with:

```bash
uv run --locked pytest --cov --cov-report=term-missing
```

Build and check the distributions as described in `CONTRIBUTING.md`, then append
the real wheel installation check to the same measurement:

```bash
uv run --locked coverage run --append scripts/check_distribution.py
```

Append the notebook storage check without executing notebook cells:

```bash
uv run --locked coverage run --append scripts/check_notebooks.py
```

Generate the complete reports:

```bash
uv run --locked coverage report
uv run --locked coverage xml
uv run --locked coverage html
```

Open `htmlcov/index.html` for highlighted missing lines and branches. XML includes
separate line and branch rates. With branch measurement enabled, the terminal's
`Cover` column is a combined line/branch figure; it is not the line-only rate.
The `testing` workflow prints the report and saves XML and HTML as a GitHub Actions
artifact for seven days. Generated reports and coverage data are ignored by Git.
Each pytest command above starts a new run; use `coverage run --append` only for
additional checks belonging to that run, so results do not accumulate across edits.

Tests are outside the measured source scope. There are no custom coverage
exclusions, percentage thresholds, or automatic changes to code or notebook policy.
When renaming the package, update the source path in `pyproject.toml` too.

## Optional Codecov upload

Local and GitHub artifact reporting work without Codecov. No coverage report is
sent to Codecov by the active workflow. The root `codecov.yml` disables project and
patch status checks, PR comments, and annotations; there is no coverage-dependent
failure configured.

The inactive `.github/workflow-templates/coverage.yml.example` contains the report
and upload integration. Enable the actual repository in Codecov and configure its
upload credentials before adapting that example. Keep tokens in GitHub Actions
secrets. Remove its explicit false upload condition only after deciding to enable
that transfer. A first real upload and service permissions must then be verified.

References: [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/),
[Branch coverage](https://coverage.readthedocs.io/en/latest/branch.html),
[Codecov statuses](https://docs.codecov.com/docs/commit-status),
[Codecov Action](https://github.com/codecov/codecov-action).
