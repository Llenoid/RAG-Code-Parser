FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Pin pip and set environment variables for stability
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure code volume exists for volume mounting
RUN mkdir -p /app/code

# Temporary entrypoint for TDD phase.
# We will transition this to a CLI entrypoint in Phase 5.
