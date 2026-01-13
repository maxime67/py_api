from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import AsyncSessionLocal

# Injection de dépendances de la session SQLAlchemy (ORM)
async def get_db() -> AsyncSession:
    """
    Dependency that provides a database session for a single request.
    """
    async with AsyncSessionLocal() as session:
        yield session
