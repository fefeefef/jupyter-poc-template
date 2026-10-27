# Template configuration

## Python and dependencies

Python 3.11 is used in CI and by the code-quality tools. `pyproject.toml` contains
package metadata and dependency groups; `uv.lock` records resolved dependency
versions. Keep the Python requirement, Ruff target, and CI version consistent.

Setuptools builds the `src` package and is pinned in `[build-system]`.
Pre-Commit installs versioned hooks in separate environments and resolves their
transitive dependencies independently of `uv.lock`.

JupyterLab and ipykernel are optional dependencies in the `notebook` extra.
CI checks notebook files without installing or running a notebook kernel.

## Code quality

Ruff checks Python and notebook source. The formatter uses a 100-character
target; E501 is not selected.
The selected lint rules are listed and described in `pyproject.toml`.

The Ruff hook applies safe corrections for I001, W291, W292, W293, F401, RUF100,
UP006, and UP007. Other selected violations fail the check. Ruff formatting,
pyupgrade, and file hygiene hooks apply their own corrections. Review and stage
changes made by hooks before retrying a commit.

File hooks check added files over 1,000 KB, filename case conflicts, executable
and shebang consistency, JSON, TOML, YAML, merge conflicts, symlinks, debug
statements, private-key patterns, line endings, test filenames, and whitespace.

Pre-Commit installs file and commit-message hooks. Commit messages require a scope
and one of `chore`, `ci`, `docs`, `feat`, `fix`, or `test`. CI runs file hooks;
it does not validate commit messages or commit automatic corrections.

## Notebooks

The notebook checker uses nbformat to validate structure and rejects saved outputs,
non-null execution counts, attachments, and widget state. It does not execute
cells, evaluate analysis results, or scan source text for confidential values.

## Automation and documentation

The `testing` workflow runs hooks, tests, package builds, distribution checks, and
the Sphinx documentation build on pushes and pull requests. GitHub Actions use
commit-pinned versions, and CI installs uv 0.13.5.

Line and branch coverage includes the package and its own scripts. Reports are
informational and have no percentage gate. Codecov uploads run when the repository
variable `CODECOV_ENABLED` is `true`; otherwise reports remain local and in GitHub
Actions artifacts.

Sphinx builds documentation, including API references from docstrings. MyST
supports Markdown pages. Documentation deployment and package publishing are
disabled. The publishing example is outside the active workflows directory.

Dependabot is configured for weekly `uv` and GitHub Actions update pull requests.
See `TEMPLATE_SETUP.md` for project identity, license, and security setup.

Git ignore patterns cover common credential, data, and generated artifact paths.
Review changes for sensitive content before committing.
