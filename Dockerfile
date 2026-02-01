FROM python:3.11-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock* /app/

# Install dependencies with uv
RUN uv sync --frozen --no-cache && rm -rf /root/.cache

# Copy project
COPY . /app/

# Expose port
EXPOSE 8000