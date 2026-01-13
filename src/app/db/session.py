from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Configuration conditionnelle de l'engine
if "sqlite+aiosqlite" in settings.DATABASE_URL:
    # Configuration pour SQLite basé sur un fichier
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=True,
        connect_args={"check_same_thread": False} # Requis pour SQLite
    )
else:
    # Configuration par défaut pour les autres BDD (ex: mysql+asyncmy, postgresql+asyncpg, etc.)
    engine = create_async_engine(settings.DATABASE_URL, echo=True)

# SessionMaker pour créer des sessions asynchrones
# expire_on_commit=False est important pour utiliser les objets après le commit dans un contexte async
AsyncSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession, expire_on_commit=False
)
