FROM python:3.11-slim@sha256:65bd3d9f1d7fa268dd1909973ba7eb4bdf41f6dcf2cfbe76ba9528b170f3fd79

WORKDIR /app

COPY requirements.txt .

# The base image bundles setuptools and wheel, which carry fixable High CVEs
# that fail the image scan. Every dependency installs as a wheel and nothing
# imports them at runtime, so they go once the install is done.
RUN pip install --no-cache-dir -r requirements.txt \
    && pip uninstall -y setuptools wheel

COPY src/mountaineers_activity_scraper /app/mountaineers_activity_scraper

ENTRYPOINT ["python3", "-m", "mountaineers_activity_scraper.cli"]
