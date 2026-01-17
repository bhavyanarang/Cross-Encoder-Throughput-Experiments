FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
COPY conf/ conf/
COPY scripts/ scripts/

ENTRYPOINT ["python", "-m", "src.main"]
