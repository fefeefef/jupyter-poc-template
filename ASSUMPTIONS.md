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
- GitHub Actions runs the Pre-Commit hooks and validates pushes and pull requests only. No CD, publication, or release automation is included.
- Project name, description, responsible team, and license are unresolved TODOs. No license is assumed.
- CLA policy is separate and is not activated by this template.
