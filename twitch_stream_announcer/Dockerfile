FROM ghcr.io/astral-sh/uv:python3.12-alpine

COPY uv.lock pyproject.toml /root/stream_announcer/

WORKDIR /root/stream_announcer
RUN uv sync --no-dev --frozen --no-cache --no-install-project

COPY src /root/stream_announcer/src

ENV PYTHONPATH=$PYTHONPATH:/root/stream_announcer/src

CMD ["uv", "run", "--no-dev", "python", "src/stream_announcer.py"]
