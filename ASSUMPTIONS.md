# Template assumptions

- This is an optional starting point for a new customer PoC repository. Existing organization and customer rules take precedence.
- Python 3.11, uv, and a committed uv.lock are starting choices, not inferred organization standards. Align requires-python, Ruff target, CI version, and dependency workflow with each PoC.
- pyproject.toml holds project metadata. setuptools is used for the small src-layout helper package.
- JupyterLab and ipykernel are optional notebook dependencies; CI does not install or execute them.
- Ruff checks Python and notebook source using all current stable Pyflakes (F) rules and selected import, whitespace, bug prevention, pytest, suppression, Ruff-specific, and type modernization rules. Each rule is explicitly listed and documented in pyproject.toml; review the selection when upgrading Ruff. The formatter uses a 100-character target; E501 is not selected. These are template choices, not organization-wide standards.
- The local Ruff lint hook uses --fix, but automatic corrections are limited to safe fixes for I001, W291, W292, W293, F401, RUF100, UP006, and UP007. Other selected violations fail the hook. Unsafe fixes are not enabled. Review and stage hook changes before retrying a commit.
- Ruff formatting is checked rather than automatically applied. Pre-Commit also checks basic file hygiene. The same hooks run in CI; corrections made during a CI run cause the hook check to fail rather than being committed automatically.
- pytest checks the local notebook policy script, which uses nbformat for schema validation. Neither the lint checks nor the policy tests execute notebook cells or verify the analysis results.
- The empty-output notebook policy is a customer-PoC safeguard selected for this template, not an inferred organization-wide rule. It rejects outputs, non-null execution counts, attachments, and saved widget state. It does not inspect notebook source for sensitive values.
- Git ignore rules reduce accidental commits of common data, credential, and artifact files. They cannot guarantee confidentiality; human review remains required.
- GitHub Actions runs the Pre-Commit hooks and validates pushes and pull requests only. No CD, publication, or release automation is included.
- Project name, description, responsible team, and license are unresolved TODOs. No license is assumed.
- CLA policy is separate and is not activated by this template.
