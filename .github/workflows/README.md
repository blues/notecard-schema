# GitHub Workflows

## `ci.yml` — Validation

Runs the pre-commit hooks and `pytest` on pushes to `master` and on pull
requests targeting `master`. All schemas must pass before merge.

## `publish-docs.yml` — Schema reference site

Runs `scripts/generate_docs.py` and `mkdocs build`, then deploys the resulting
static site to GitHub Pages. This site is aimed at LLM agents; the
human-facing API reference is built elsewhere (see `update-hook.yml` below).

Triggers:

- a successful CI run on `master`
- a push to `master` touching any `.json` file or `scripts/generate_docs.py`
- manual dispatch

## `release-schema.yml` — Release asset

On a published release, stamps the release version into the `version` property
of every schema, rewrites `notecard.api.json` so its `$ref`s and `$id` point at
the tagged refs instead of `master`, and uploads that file as a release asset.

## `update-hook.yml` — Downstream notification

On a published release (or manual dispatch), notifies each repository that
consumes these schemas so it can regenerate its own derived artifacts — client
library code, and the
[Notecard API Reference](https://dev.blues.io/api-reference/notecard-api/)
documentation. Neither the documentation rendering nor the generated client code
lives in this repository; each consumer owns its generator and opens its own
pull request.

### Setup

The dispatch authenticates with a GitHub App installed on the consuming
repositories, configured through two repository secrets:

- `SCHEMA_SYNC_APP_ID`
- `SCHEMA_SYNC_PRIVATE_KEY`

The App needs `contents: write` and `pull-requests: write` on those repositories
so it can trigger workflows that branch, commit, and open PRs.

### Troubleshooting

- **Dispatch fails with 404** — the App is not installed on the consuming
  repository, or the workflow it triggers is missing from that repository's
  default branch.
- **Dispatch succeeds but no pull request appears** — normal when the schemas
  produce no output change; check the run on the consuming side to confirm.
- **Token errors** — verify the App ID and private key secrets, and that the
  App's installation still covers every consumer.
- One consumer failing does not block the others; the matrix uses
  `fail-fast: false`.

## `copilot-setup-steps.yml` — Copilot environment

Manual dispatch only. Installs Python 3.13 and the dev dependencies, then runs
`scripts/update_schema_version.py --help` as a smoke test, so GitHub Copilot's
coding agent can pick up a working environment definition. The job name must
stay `copilot-setup-steps` for Copilot to find it.
