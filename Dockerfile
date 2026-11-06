FROM python:3.11-slim@sha256:65bd3d9f1d7fa268dd1909973ba7eb4bdf41f6dcf2cfbe76ba9528b170f3fd79

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/mountaineers_activity_scraper /app/mountaineers_activity_scraper

ENTRYPOINT ["python3", "-m", "mountaineers_activity_scraper.cli"]
