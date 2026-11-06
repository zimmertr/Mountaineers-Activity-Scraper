# Contributing

Every merge to `main` releases a new image that the cluster runs the next night, so changes come through PRs that TJ reviews.

1. Branch from the latest `main`.
2. Make one change per PR, and title it `type(scope): summary`, such as `fix(scraper): handle a missing leader`. The type sets the release: `feat` is a minor, `fix` and most others a patch, and a `!` a major.
3. Build and run it in Docker, as the README shows.
4. Open the PR. `Docker Build` builds, scans and smoke-tests the image, and the `Release` dry run says what the merge will release ([docs/CICD.md](docs/CICD.md)).

Never commit `google_cloud_credentials.json` or the URL lists.
