FROM python:3.11-slim

WORKDIR /app

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
CMD ["pytest"]
