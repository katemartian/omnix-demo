# syntax=docker/dockerfile:1
FROM python:3.10-slim

# System deps for FAISS & sentence-transformers
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential git curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy only metadata first to leverage Docker cache
COPY pyproject.toml README.md ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e .[dev]

# Copy source and data
COPY src ./src
COPY data ./data
COPY contracts ./contracts
COPY app ./app

# Expose FastAPI port
EXPOSE 8000

# Default: start API
CMD ["python", "-m", "omnix.api"]
