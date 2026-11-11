# Mountaineers-Activity-Scraper

A Python CLI that collects activity URLs from The Mountaineers' site, scrapes each one, and writes the results to a Google Sheet. It runs as a nightly CronJob from zimmertr/Kubernetes-Manifests (`misc/mountaineers-activity-scraper`). Start with [`docs/CICD.md`](docs/CICD.md).

This repo took a trimmed set of the files a new project starts with (zimmertr/yggdrasil record 0038). When a change here makes a decision, write its record under `docs/architectural-decision-records/`; when it needs a page `docs/` doesn't have yet, add it in the same PR.

## Rules

- **A merge is a release.** Every merge to `main` pushes a new image and opens a self-merging Kubernetes-Manifests PR, so the next nightly run uses it. The PR title sets the version bump.
- **No credentials in the repo.** `google_cloud_credentials.json` and the URL lists are gitignored; the cluster mounts the credentials from a Secret.
- **Build and run in Docker,** as the README shows.
- The README is TJ's: keep it accurate and in his voice, and never restructure it.

## Issues

File issues with the `create-issue` skill from zimmertr/ai-config: the two-sentence summary, the six sections, the hemingway and humanizer passes, one priority, one type, the area labels and the session label. The skill reads the four things below from this section.

- **The reader**: TJ, who climbs with The Mountaineers and reads Python.
- **The gates**: `Docker Build / Docker Build`, `PR Title / PR Title` and the three `Lint /` checks pass; the docs page that owns the topic changes in the same PR; the README changes only to stay accurate.
- **The constraints**: no credentials in the repo or in logs; the image stays linux/amd64, which the cluster runs.
- **The areas**: `scraper` (`src/`), `ci` (the workflows, the image and Renovate), `security`.

## Working in this repo

- Work in a fresh clone in the session's scratchpad, never in TJ's checkout. Branch from the latest `origin/main`.
- Everything reaches main through a squash-merged PR. Never push to main.
- The PR title is `type(scope): summary`; the `PR Title` check refuses anything else.
- Actions are pinned to commit SHAs with the version in a comment, and the base image to its tag and digest. Renovate bumps both.
