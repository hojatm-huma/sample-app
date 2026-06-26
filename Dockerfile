FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

COPY .python-version \
     main.py \
     pyproject.toml \
     ./

RUN uv sync

CMD ["uv", "run", "main.py"]
