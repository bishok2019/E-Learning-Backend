# FROM python:3.11-slim

# # Install uv
# COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# # Set environment variables
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# # Set work directory
# WORKDIR /app

# # Copy dependency files
# COPY pyproject.toml uv.lock* /app/

# # Install dependencies with uv
# RUN uv sync --frozen --no-cache && rm -rf /root/.cache

# # Copy project
# COPY . /app/

# # Expose port
# EXPOSE 8000




FROM python:3.11-slim

# Install PostgreSQL client (for pg_isready)
RUN apt-get update && \
    apt-get install -y postgresql-client && \
    rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Environment settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Work directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock* /app/

# Install dependencies
RUN uv sync --frozen --no-cache && rm -rf /root/.cache

# Copy project files
COPY . /app/

# Expose port
EXPOSE 8000
