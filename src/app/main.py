from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.config import settings
from app.db.session import engine, AsyncSessionLocal
from app.api.routers.opinions import router as opinions_router
from app.api.routers.movies import router as movies_router
from app.api.routers.genres import router as genres_router
from app.api.routers.participants import router as participants_router
from app.models import Base
from app.core.exceptions import NotFoundBLLException, ValidationBLLException, DALException, BLLException
from app.api.exception_handlers import (
    not_found_bll_exception_handler,
    validation_bll_exception_handler,
    dal_exception_handler,
    bll_exception_handler,
)
from app.db.seeding import seed_db

@asynccontextmanager
async def lifespan(myapp: FastAPI):
    # Création des tables au démarrage
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # Seeding conditionnel (désactivé en production via SEED_DATABASE=false)
    if settings.SEED_DATABASE:
        async with AsyncSessionLocal() as session:
            await seed_db(session)
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Une API pour gérer une collection de films, réalisée avec FastAPI et SQLAlchemy async.",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(opinions_router, prefix=settings.API_V1_STR, tags=["Opinions"])
app.include_router(movies_router, prefix=settings.API_V1_STR, tags=["Movies"])
app.include_router(genres_router, prefix=settings.API_V1_STR, tags=["Genres"])
app.include_router(participants_router, prefix=settings.API_V1_STR, tags=["Participants"])

# Ajouter les gestionnaires d'exceptions
app.add_exception_handler(NotFoundBLLException, not_found_bll_exception_handler)
app.add_exception_handler(ValidationBLLException, validation_bll_exception_handler)
app.add_exception_handler(DALException, dal_exception_handler)
app.add_exception_handler(BLLException, bll_exception_handler)

@app.get("/", tags=["Root"])
def read_root():
    """Endpoint racine pour vérifier que l'API est en ligne."""
    return {"message": "Welcome to this fantastic API!"}


@app.get("/health", tags=["Health"])
def health_check():
    """Endpoint de santé pour Kubernetes liveness/readiness probes."""
    return {"status": "healthy"}

