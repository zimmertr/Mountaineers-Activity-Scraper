# CI/CD

Every workflow calls a zimmertr/yggdrasil module, pinned by commit SHA.

| Workflow | Runs on | What it does |
|---|---|---|
| [`pr.yml`](../.github/workflows/pr.yml) | PRs | `docker-build`: hadolint, the linux/amd64 image built but not pushed, a Trivy table in a sticky comment, container-structure-test running [`tests/structure-test.yaml`](../tests/structure-test.yaml) (the entry point and working directory, `--help`, and an import of every dependency), and a failure on any fixable Critical or High. |
| [`release.yml`](../.github/workflows/release.yml) | merges to `main`, and PRs as a dry run | `release`: GitVersion reads the bump from the squash commit's title, pushes `ghcr.io/zimmertr/mountaineers-activity-scraper:<version>`, scans it, tags and releases the commit, then opens a self-merging Kubernetes-Manifests PR that sets the CronJob's `newTag` and its `digest`, so the cluster runs the bytes the release scanned (yggdrasil's record 0052). On a PR it only says, in the job summary, what the merge will release. |
| [`pr-title.yml`](../.github/workflows/pr-title.yml) | PRs | `pr-title`: the title must be `type(scope): summary`. |
| [`lint.yml`](../.github/workflows/lint.yml) | PRs | `lint`: actionlint, zizmor's pedantic audits, and Semgrep's rule that the Dockerfile's `FROM` carries a digest. |
## Secrets

- `GH_PAT` (Actions): contents and pull-requests write on Kubernetes-Manifests, for the bump PR.

## Renovate

[`renovate.json`](../.github/renovate.json) extends zimmertr/yggdrasil's shared preset (its record 0056). Renovate proposes new versions of the pinned actions and of the Python base image, each seven days after it ships; yggdrasil's own modules don't wait. Everything below a major merges itself once the required checks pass, and a major waits for TJ. `requirements.txt` isn't pinned, so each build installs the latest packages and Renovate has nothing to propose there.
