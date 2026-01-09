# syntax = docker/dockerfile:1.2
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim


RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1

ENV UV_LINK_MODE=copy

# Use a writable cache directory inside the image to avoid buildkit writing to /root
ENV UV_CACHE_DIR=/app/.cache/uv

# Ensure cache dir exists
RUN mkdir -p /app/.cache/uv

COPY uv.lock pyproject.toml /app/
RUN uv sync --locked --no-install-project --no-dev

COPY . /app
RUN uv sync --locked --no-dev

ENV PATH="/app/.venv/bin:$PATH"
