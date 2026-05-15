FROM python:3.12-slim

# Prevent Python from writing .pyc files and enable unbuffered stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy system requirements
COPY requirements.txt /app/

# Upgrade pip and install dependencies
RUN pip install --upgrade pip setuptools wheel

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy application code
COPY . /app/

COPY portal/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=portal.settings

ENTRYPOINT ["/entrypoint.sh"]
