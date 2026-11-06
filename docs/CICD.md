# CI/CD

Every workflow calls a zimmertr/yggdrasil module, pinned by commit SHA.

| Workflow | Runs on | What it does |
|---|---|---|
| [`pr.yml`](../.github/workflows/pr.yml) | PRs | `docker-build`: hadolint, the linux/amd64 image built but not pushed, a Trivy table in a sticky comment, the smoke test, and a failure on any fixable Critical or High. |
| [`release.yml`](../.github/workflows/release.yml) | merges to `main`, and PRs as a dry run | `release`: GitVersion reads the bump from the squash commit's title, pushes `zimmertr/mountaineers-activity-scraper:<version>` to Docker Hub, scans it, tags and releases the commit, then opens a self-merging Kubernetes-Manifests PR that sets the CronJob's `newTag`. On a PR it only says, in the job summary, what the merge will release. |
| [`pr-title.yml`](../.github/workflows/pr-title.yml) | PRs | `pr-title`: the title must be `type(scope): summary`. |
| [`lint.yml`](../.github/workflows/lint.yml) | PRs | `lint`: actionlint, zizmor's pedantic audits, and Semgrep's rule that the Dockerfile's `FROM` carries a digest. |
| [`dependabot-auto-merge.yml`](../.github/workflows/dependabot-auto-merge.yml) | Dependabot's PRs | `auto-merge`: a patch or minor merges itself once the required checks pass. Majors and digest-only updates wait for TJ. |

## Secrets

- `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` (Actions): push the image.
- `GH_PAT` (Actions): contents and pull-requests write on Kubernetes-Manifests, for the bump PR.
- `AUTO_MERGE_PAT` (Dependabot): arms the merge. A merge made with `GITHUB_TOKEN` would start no release.

## Dependabot

[`dependabot.yml`](../.github/dependabot.yml) proposes new versions of the pinned actions and of the Python base image, daily, each three days after it ships. `requirements.txt` isn't pinned, so each build installs the latest packages and Dependabot has nothing to propose there.
