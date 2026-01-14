FROM python:3.13-slim AS builder

WORKDIR /app

# Installer uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copier les fichiers de dépendances
COPY pyproject.toml uv.lock* ./

# Installer les dépendances (sans dev)
RUN uv sync --frozen --no-cache --no-dev

# --- Image finale ---
FROM python:3.13-slim

WORKDIR /app

# Créer un utilisateur non-root pour la sécurité
RUN groupadd --gid 1000 appgroup && \
    useradd --uid 1000 --gid appgroup --shell /bin/bash appuser

# Copier uv et les dépendances depuis le builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/pyproject.toml /app/uv.lock* ./

# Copier le code source
COPY ./src/app /app/app

# Variables d'environnement avec valeurs par défaut
ENV ENVIRONMENT=production \
    HOST=0.0.0.0 \
    PORT=8000 \
    WORKERS=1 \
    LOG_LEVEL=info \
    DATABASE_URL=sqlite+aiosqlite:///./data/app.db \
    DATABASE_ECHO=false \
    DATABASE_POOL_SIZE=5 \
    DATABASE_POOL_RECYCLE=3600 \
    SEED_DATABASE=false \
    PROJECT_NAME="API Filmotheque" \
    API_V1_STR=/api/v1

# Créer le répertoire pour les données SQLite et donner les permissions
RUN mkdir -p /app/data && chown -R appuser:appgroup /app

# Passer à l'utilisateur non-root
USER appuser

# Exposer le port (valeur par défaut, peut être surchargée)
EXPOSE 8000

# Health check pour Kubernetes
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:${PORT}/health')" || exit 1

# Lancer l'application avec uvicorn
CMD uv run uvicorn app.main:app --host ${HOST} --port ${PORT} --workers ${WORKERS} --log-level ${LOG_LEVEL}
