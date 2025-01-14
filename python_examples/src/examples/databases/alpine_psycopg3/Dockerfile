FROM ghcr.io/astral-sh/uv:python3.12-alpine AS base

# Install dependencies
COPY uv.lock pyproject.toml ./
RUN uv sync --no-dev --frozen --no-cache --no-install-project

COPY main.py ./
CMD ["uv", "run", "python", "main.py"]
