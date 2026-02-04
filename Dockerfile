# 1. Base image
FROM python:3.13-slim

# 2. Install PostgreSQL client (for pg_isready)
RUN apt-get update && \
    apt-get install -y postgresql-client && \
    rm -rf /var/lib/apt/lists/*

# 3. Install uv (package manager)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# 4. Workdir
WORKDIR /app

# 5. Copy only dependency files first
COPY pyproject.toml uv.lock* /app/

# 6. Install dependencies (this layer will be cached if pyproject.toml/uv.lock didn’t change)
RUN uv sync --frozen

# 7. Set virtual environment as default
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# 8. Copy the rest of the project
COPY . /app/

# 9. Expose port
EXPOSE 8000
