FROM ghcr.io/astral-sh/uv:python3.12-alpine AS base

# Install npm for prisma
RUN apk update \
    && apk upgrade \
    && apk add --no-cache npm

COPY uv.lock pyproject.toml /root/fastapi_server/

WORKDIR /root/fastapi_server
RUN uv sync --no-dev --frozen --no-cache --no-install-project

# Prepare prisma client and generate types
COPY prisma/* /root/fastapi_server/prisma/
RUN uv run --no-dev --frozen prisma generate

COPY src /root/fastapi_server/src

RUN rm -r \
    /usr/bin/node \
    /usr/lib/node_modules \
    /root/.npm \
    /root/.cache/prisma \
    # Required for interaction with prisma: /root/.cache/prisma-python \
    /var/cache

# Squash image with trick https://stackoverflow.com/a/56118557/10882657
FROM scratch
COPY --from=base / /
WORKDIR /root/fastapi_server
ENV PYTHONPATH=$PYTHONPATH:/root/fastapi_server/src
CMD ["uv", "run", "--no-dev", "litestar", "--app-dir", "src", "run", "--host", "0.0.0.0", "--port", "8000"]
