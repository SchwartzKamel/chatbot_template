# Builder stage
FROM python:3.12-slim-bullseye AS builder

# Install system dependencies required for build
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    libssl-dev \
    libffi-dev \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry
ENV POETRY_VERSION=1.8.2
RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

# Configure Poetry
WORKDIR /app
COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.in-project true

# Install dependencies
RUN poetry export --without-hashes -f requirements.txt -o requirements.txt && \
    pip install --no-cache-dir -r requirements.txt && \
    /app/.venv/bin/pip install --no-cache-dir -r requirements.txt && \
    /app/.venv/bin/pip install --no-cache-dir google-adk && \
    pip install --no-cache-dir google-adk && \
    python3 -m pip install --target=/app/.venv/lib/python3.12/site-packages google-adk && \
    python3 -m pip install --target=/usr/local/lib/python3.12/site-packages google-adk

# Runtime stage
FROM python:3.12-slim-bullseye AS runtime

# Runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends libssl-dev && \
    rm -rf /var/lib/apt/lists/*

# Security settings
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PATH="/home/appuser/.local/bin:$PATH"

# Create non-root user
RUN groupadd -g 1000 appuser && \
    useradd -u 1000 -g appuser -d /app appuser && \
    mkdir -p /app && \
    chown appuser:appuser /app

WORKDIR /app

# Copy from builder
COPY --from=builder --chown=appuser:appuser /app/.venv /app/.venv
COPY --from=builder --chown=appuser:appuser /app/.venv/lib/python3.12/site-packages /app/.venv/lib/python3.12/site-packages
# Copy google_adk from both venv and global site-packages if present
# Copy google_adk from both venv and global site-packages if present
RUN python3 -m pip install --no-cache-dir google-adk --upgrade && \
    /app/.venv/bin/pip install --no-cache-dir google-adk --upgrade
COPY --from=builder --chown=appuser:appuser /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder --chown=appuser:appuser /usr/local/bin /usr/local/bin
ENV PATH="/app/.venv/bin:$PATH:/usr/local/bin" \
    PYTHONPATH="/app/.venv/lib/python3.12/site-packages:/usr/local/lib/python3.12/site-packages" \
    VIRTUAL_ENV="/app/.venv"
COPY --chown=appuser:appuser . .

# Security hardening
RUN find /app -type d -exec chmod 755 {} \; && \
    find /app -type f -exec chmod 644 {} \; && \
    chmod +x /app/entrypoint.sh

USER appuser

# Container security settings
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Security hardening
RUN set -eux; \
    rm -rf /var/lib/apt/lists/*; \
    chmod 755 /app/entrypoint.sh

# Runtime security configuration
VOLUME ["/tmp"]
ENTRYPOINT ["/app/entrypoint.sh"]

# Security flags (to be used in runtime)
# docker run --read-only --security-opt=no-new-privileges:true --cap-drop=ALL --cap-add=CHOWN,NET_BIND_SERVICE
