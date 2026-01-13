from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import app.models.genre as models
from sqlalchemy.exc import SQLAlchemyError
from app.core.exceptions import DALException

async def get_genres(db: AsyncSession):
    """Récupère tous les genres de la base de données."""
    try:
        stmt = select(models.Genre)
        result = await db.execute(stmt)
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise DALException("Erreur lors de la récupération des genres", original_exception=e)
