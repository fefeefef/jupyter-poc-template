# Set up a project from this template

This document is for the person creating a repository. The README is for the
users of the resulting package. Complete this checklist before presenting the
adapted repository as a finished project, then remove or archive this setup guide.

## Identity and installation

1. Copy the template files without `.git`, `.venv`, caches, or generated artifacts,
   or use GitHub's template feature once an owner enables it for the repository.
2. Replace the distribution name, description, authors, and version in
   `pyproject.toml`. Rename `src/project_name`; update imports in tests, the README,
   the notebook if present, documentation, and `scripts/check_distribution.py`.
   The distribution name and Python import name may differ.
3. Replace the example `greet` API and its tests with your actual public API and
   a minimal, runnable example. Update the wheel smoke check to exercise that API.
4. Run `uv lock`, then the locked setup and checks in `CONTRIBUTING.md`.
   `uv build` must create a wheel and source distribution; `twine check` validates
   their metadata. `MANIFEST.in` includes the repository scripts needed by the tests
   shipped in the source distribution. The distribution smoke check uses a fresh virtual environment,
   installs the local wheel, and imports it outside the checkout. Its `--no-deps`
   installation is appropriate for this dependency-free starter only; when adding
   runtime dependencies, arrange their installation in the smoke environment too.
5. Replace `YOUR_PACKAGE_NAME` in the pip instructions only with the real published
   distribution name. Before publication, use `python -m pip install .` locally.

## Public GitHub page

- Replace the README title, description, features, and quickstart.
- The commented badge block contains optional paper/arXiv, Hugging Face, PyPI,
  download, documentation, license, testing, and Codecov links. Replace each
  placeholder and enable only links that actually exist for your project.
- Paper, model hosting, and download counts are not required for every package.
  Do not copy TiRex-2 identifiers or advertise a service that has not been set up.
- Sphinx is configured from the explicit tool named in the feedback. Update
  `docs/conf.py`, the API reference, and documentation links when adapting the package.
- Issue forms intentionally avoid labels that might not exist in a newly created
  repository. Add the desired labels and assignments only after creating them.

## Ownership, license, and security

- `LICENSE` is intentionally zero bytes as requested. Have the project owners
  select an approved license, populate the file, and update package metadata and
  the README before public release. No license is inferred from TiRex-2.
- Replace the TODOs in `SECURITY.md`: supported releases, a monitored private
  reporting channel, and any agreed response expectations. Enable GitHub private
  vulnerability reporting if it is the chosen channel, and verify it works.
- Confirm the applicable CLA policy with the responsible team. This template does
  not activate or assert an organization-specific CLA requirement.
- Dependabot is configured for weekly `uv` and GitHub Actions updates. Review its
  first PR and confirm that it updates the manifest and lockfile consistently.
- Branch protection, required checks, scanning, repository visibility, and service
  permissions are repository settings. They are not established by these files.
  Confirm the intended settings with the owners rather than assuming that the
  phrase “same security as TiRex-2” authorizes additional policies.
- If required checks already exist, update them deliberately after the workflow
  rename to `testing`. GitHub commonly identifies a check by its job name (`checks`),
  so inspect actual check names instead of guessing from the filename.

## Documentation and coverage

Sphinx was explicitly confirmed after discussing it with the user. Update
`docs/conf.py`, the API reference, and the user pages for the adapted project.
The site is built locally and in testing; it is not deployed.

Line and branch coverage for the package and own scripts is explicitly enabled
for reporting only. Update the package source path in `[tool.coverage.run]` when
renaming it. The 95 → 99 → 100 percent goal is not a configured threshold, warning,
or merge condition. Review coverage alongside the behavior and assertions being
tested rather than treating the number as proof of quality.

`testing` prints coverage and saves XML/HTML reports as GitHub artifacts.
`codecov.yml` disables Codecov project and patch statuses and automated comments.
The upload step in `testing` is off unless the repository Actions variable
`CODECOV_ENABLED` is `true`. Configure Codecov and any required repository upload
secret before enabling it. Public repositories that already permit tokenless
uploads need no secret. See `docs/coverage.md` for activation and verification;
no separate coverage workflow needs to be enabled.

## Publishing

There is no active publishing or deployment workflow. A future publishing workflow
was mentioned in the original notes, but active CD is outside the current scope.
No release, package upload, documentation deployment, or external account setup is
performed by this template. See `docs/publishing.md` for a deliberately inactive
preparation example and the decisions required before activation.

## Final check

Review placeholders with a repository search such as:

```bash
rg -n 'TODO|YOUR_PACKAGE_NAME|DISTRIBUTION_NAME|OWNER|REPOSITORY|ARXIV_ID|LICENSE_ID|project_name' . .github
```

Run all documented checks from a fresh checkout. Verify the README's rendered
links, the issue forms, the PR template, and an actual `testing` run on GitHub.
Never treat placeholder completion or successful local checks as proof of live
GitHub settings or third-party integration.
