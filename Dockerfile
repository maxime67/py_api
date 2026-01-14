# syntax=docker/dockerfile:1
FROM python:3.13-slim

# Métadonnées
LABEL maintainer="maxxa"
LABEL description="FastAPI REST API pour la gestion de films"

# Variables d'environnement pour Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1

# Variables d'environnement par défaut (peuvent être surchargées)
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

# Répertoire de travail
WORKDIR /app

# Installer uv pour la gestion des dépendances
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copier les fichiers de configuration des dépendances
COPY pyproject.toml uv.lock* ./

# Installer les dépendances (production uniquement)
RUN uv sync --frozen --no-cache --no-dev

# Copier le code de l'application
COPY ./src/app ./app

# Créer un utilisateur non-root pour la sécurité
RUN adduser --disabled-password --gecos "" --uid 1000 appuser && \
    mkdir -p /app/data /home/appuser/.cache/uv && \
    chown -R appuser:appuser /app /home/appuser

USER appuser

# Exposer le port
EXPOSE ${PORT}

# Health check pour Kubernetes
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:${PORT}/health')" || exit 1

# Commande de démarrage avec uvicorn pour la production
CMD ["sh", "-c", "uv run uvicorn app.main:app --host ${HOST} --port ${PORT} --workers ${WORKERS} --log-level ${LOG_LEVEL}"]
