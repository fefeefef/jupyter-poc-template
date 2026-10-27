# Package publishing

Publishing is disabled. `.github/workflow-templates/publish.yml.example` is an
inactive example outside `.github/workflows/`. It has a `.example` extension and
both jobs have `if: ${{ false }}`. No upload action or destination is configured.

The example separates package building and metadata checks from uploading.
The `testing` workflow builds and validates distributions without publishing them.

## Configuration

To configure a publishing workflow:

1. Set the package index, distribution name, version, license, and package metadata.
2. Set the release trigger and required build and test steps.
3. Configure authentication, such as Trusted Publishing/OIDC, for the package index.
4. Transfer the checked artifacts from the build job to the publishing job and
   configure the upload action.
5. Place the completed workflow in `.github/workflows/` with a `.yml` extension
   and replace the disabled job conditions with the release conditions.

Renaming the example alone does not enable package uploads.

References: [PyPA publishing guide](https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/),
[GitHub workflow activation](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/disable-and-enable-workflows).
