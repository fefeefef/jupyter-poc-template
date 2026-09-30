# Template assumptions

- This is an optional starting point for a new customer PoC repository. Existing organization and customer rules take precedence.
- Python 3.11, uv, and a committed uv.lock are starting choices, not inferred organization standards. Align requires-python, Ruff target, CI version, and dependency workflow with each PoC.
- pyproject.toml holds project metadata. setuptools is used for the small src-layout helper package.
- JupyterLab and ipykernel are optional notebook dependencies; CI does not install or execute them.
- Ruff checks Python and notebook files using a proposed E, F, I, and UP baseline. Pre-Commit also runs basic file hygiene checks. pytest checks the local notebook policy script, which uses nbformat for schema validation.
- The empty-output notebook policy is a customer-PoC safeguard selected for this template, not an inferred organization-wide rule. It rejects outputs, non-null execution counts, attachments, and saved widget state. It does not inspect notebook source for sensitive values.
- Git ignore rules reduce accidental commits of common data, credential, and artifact files. They cannot guarantee confidentiality; human review remains required.
- GitHub Actions runs the Pre-Commit hooks and validates pushes and pull requests only. No CD, publication, or release automation is included.
- Project name, description, responsible team, and license are unresolved TODOs. No license is assumed.
- CLA policy is separate and is not activated by this template.
