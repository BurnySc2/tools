FROM ghcr.io/astral-sh/uv:python3.12-alpine AS base

WORKDIR /root
# Install dependencies
COPY uv.lock pyproject.toml ./
RUN uv sync --no-dev --frozen --no-cache --no-install-project

COPY main.py ./
ENV PATH="/root/.venv/bin:$PATH"
CMD ["python", "main.py"]
