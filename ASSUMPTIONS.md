# Template assumptions

- This is an optional starting point for a new customer PoC repository. Existing organization and customer rules take precedence.
- Python 3.11, uv, and a committed uv.lock are starting choices, not inferred organization standards. Align requires-python, Ruff target, CI version, and dependency workflow with each PoC.
- pyproject.toml holds project metadata. setuptools is used for the small src-layout helper package.
- JupyterLab and ipykernel are optional notebook dependencies; CI does not install or execute them.
- Ruff checks Python and notebook source using all current stable Pyflakes (F) rules and selected import, whitespace, bug prevention, pytest, suppression, Ruff-specific, and type modernization rules. Each rule is explicitly listed and documented in pyproject.toml; review the selection when upgrading Ruff. The formatter uses a 100-character target; E501 is not selected. These are template choices, not organization-wide standards.
- The pinned Ruff lint hook uses --fix, but automatic corrections are limited to safe fixes for I001, W291, W292, W293, F401, RUF100, UP006, and UP007. Other selected violations fail the hook. Unsafe fixes are not enabled. Review and stage hook changes before retrying a commit.
- The Pre-Commit hook set and pinned versions follow the supplied TiRex-2 configuration, while the template-specific Ruff rules and safe-fix allowlist are retained. Ruff formatting is automatically applied. pyupgrade targets Python 3.11 and may modernize syntax beyond the selected Ruff rules; its corrections are independent of Ruff's fixable allowlist.
- File hooks also check added file sizes (1,000 KB), filename case conflicts, executable/shebang consistency, JSON, merge conflicts, symlinks, TOML, YAML, debug statements, private-key patterns, line endings, test filenames, and whitespace. The TiRex-2 helper exclusion is retained; disabled reference hooks remain disabled.
- Installing Pre-Commit enables both pre-commit and commit-msg stages. Conventional Commit messages require a scope and one of chore, ci, docs, feat, fix, or test. CI runs the file hooks without checking commit messages; corrections made during CI fail the check rather than being committed automatically.
- pytest checks the local notebook policy script, which uses nbformat for schema validation. Neither the lint checks nor the policy tests execute notebook cells or verify the analysis results.
- The empty-output notebook policy is a customer-PoC safeguard selected for this template, not an inferred organization-wide rule. It rejects outputs, non-null execution counts, attachments, and saved widget state. It does not inspect notebook source for sensitive values.
- Git ignore rules reduce accidental commits of common data, credential, and artifact files. They cannot guarantee confidentiality; human review remains required.
- GitHub Actions runs the Pre-Commit hooks, tests, package build, metadata check, isolated wheel smoke check, and documentation build on pushes and pull requests. No active CD, publication, or release automation is included; inactive preparation examples are outside the workflows directory.
- Project name, description, responsible team, and license are unresolved TODOs. No license is assumed.
- CLA policy is separate and is not activated by this template.

- The user-facing README follows the TiRex-2 structure with optional, commented badge placeholders. It does not claim an existing publication or hosted documentation.
- Sphinx follows the tool explicitly named in the feedback. MyST parses Markdown notes; documentation builds but is not deployed.
- LICENSE is an intentionally empty placeholder. Maintainers must choose the license, security contact, supported releases, and any response expectations.
- Dependabot uses the uv ecosystem to update the manifest and lockfile, plus GitHub Actions updates. This adapts the reference to the existing dependency workflow.
- Line and branch coverage of the package and own scripts was explicitly approved for reporting only. There is no minimum percentage, warning threshold, or merge gate; Codecov upload is an explicit opt-in through the repository Actions variable CODECOV_ENABLED; it defaults to off in a newly created repository.
- The workflow is named testing. Package metadata and installation of the built wheel are checked without publishing. The starter wheel has no runtime dependencies; adapt its isolated smoke check when adding dependencies.
- No additional lint rules, automatic corrections, scientific methods, or notebook failure conditions are introduced by this update. Coverage collection follows the explicit reporting-only decision.

- GitHub Actions references are pinned to verified commit SHAs. CI installs uv 0.13.5; dependency versions remain locked in uv.lock.

- The Setuptools build backend is pinned to the version verified for this starter.
  This controls the backend version without promising byte-identical builds or
  locked transitive dependencies in Pre-Commit's separate hook environments.
