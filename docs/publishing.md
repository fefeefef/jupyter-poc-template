# Future package publishing

Active CD is outside the current scope. Nothing in this repository publishes a
package or deploys documentation. The file
`.github/workflow-templates/publish.yml.example` is an inactive preparation example,
not a workflow installed in `.github/workflows/`.

It has a `.example` extension and both jobs also have an explicit false condition.
A manual trigger alone would not make a workflow fully disabled; these barriers
make the default inactive state visible in source control.

Before adapting or activating it, the owners must confirm:

1. The target package index (PyPI is only a candidate) and real package name.
2. Approved license, complete metadata, versioning, and the release trigger.
3. Build/test prerequisites and any desired human release approval.
4. Trusted Publishing/OIDC configuration and repository environment on the index.
5. Artifact transfer between the build and publish jobs.

The example keeps build/metadata checks separate from uploading. It intentionally
contains no working upload action or destination until those choices are made.
Renaming it alone does not enable package upload. The regular `testing` workflow
already builds and validates the local distributions without publishing them.

References: [PyPA publishing guide](https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/),
[GitHub workflow activation](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/disable-and-enable-workflows).
