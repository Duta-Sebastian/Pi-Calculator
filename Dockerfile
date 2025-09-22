FROM alpine:3.22.1

RUN apk add --no-cache \
    gcc \
    curl \
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && mv /root/.local /opt/uv \
    && chmod -R 755 /opt/uv

ENV PATH="/opt/uv/bin:$PATH"

RUN adduser -D -s /bin/sh appuser

WORKDIR /app

RUN chown -R appuser:appuser /app

USER appuser

COPY --chown=appuser:appuser pyproject.toml .

RUN uv sync

ENV PATH="/app/.venv/bin:$PATH"

COPY --chown=appuser:appuser . .

EXPOSE 5000