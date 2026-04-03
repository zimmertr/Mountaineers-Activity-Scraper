FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY scraper.py .
COPY date_utils.py .
COPY scraper_utils.py .
COPY sheet_manager.py .

ENTRYPOINT ["python3", "scraper.py"]
