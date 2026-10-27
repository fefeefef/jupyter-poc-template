# Coverage and Codecov

Line and branch coverage are measured for `src/project_name` and `scripts`.
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

Test files are excluded from measurement. There are no custom coverage exclusions
or percentage thresholds.
When renaming the package, update the source path in `pyproject.toml` too.

## Optional Codecov upload

The `testing` workflow contains a complete upload step. It runs only when the
repository Actions variable `CODECOV_ENABLED` is exactly `true`. New repositories
created from the template do not inherit this variable, so uploads remain off
until their owners configure and enable the integration.

To enable it for the actual repository:

1. Sign in to Codecov with the repository owner's GitHub account and select the
   repository. Confirm the account's applicable upload-authentication setting.
2. For a public repository that already permits tokenless uploads, no upload
   secret is needed. Otherwise, store its Codecov repository token in the GitHub
   Actions secret `CODECOV_TOKEN`; never commit a token. Private repositories
   require an authenticated upload. OIDC requires separate workflow permissions
   and authentication configuration.
3. In GitHub **Settings → Secrets and variables → Actions → Variables**, create
   the repository variable `CODECOV_ENABLED` with the value `true`.
4. Push a change or rerun `testing`, inspect the Codecov upload step, and verify
   that the dashboard shows the exact tested commit and correct file paths.
5. Enable the README's Codecov badge only after replacing its owner/repository
   placeholders and verifying the destination. A badge displays the service's
   reported coverage and links to its detailed report; it does not run tests.

The upload action accepts an empty token when the service permits tokenless
uploads. No account security setting is changed by the workflow. Upload failures
are visible in the logs but do not block the tests. The root `codecov.yml` keeps
project/patch statuses, PR comments, and annotations disabled; no percentage gate
is introduced. GitHub artifact reporting continues independently of Codecov.

The opt-in step in `testing` is the single Codecov upload path; no separate
coverage workflow needs to be activated or maintained.

References: [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/),
[Branch coverage](https://coverage.readthedocs.io/en/latest/branch.html),
[Codecov tokens](https://docs.codecov.com/docs/codecov-tokens),
[Codecov statuses](https://docs.codecov.com/docs/commit-status),
[Codecov Action](https://github.com/codecov/codecov-action).
