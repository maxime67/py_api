from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

import app.schemas.opinion as schemas
import app.models.opinion as models
from sqlalchemy.exc import SQLAlchemyError
from app.core.exceptions import DALException

async def create_opinion_for_movie(db: AsyncSession, opinion: schemas.OpinionCreate, movie_id: int):
    """Crée un avis pour un film donné."""
    try:
        db_opinion = models.Opinion(**opinion.model_dump(), movie_id=movie_id)
        db.add(db_opinion)
        await db.commit()
        await db.refresh(db_opinion)

        query = (
            select(models.Opinion)
            .where(models.Opinion.id == db_opinion.id)
            .options(
                selectinload(models.Opinion.member)
            )
        )
        result = await db.execute(query)
        return result.scalars().one()
    except SQLAlchemyError as e:
        await db.rollback()  # IMPORTANT: annuler la transaction en cas d'erreur
        raise DALException("Erreur lors de la création de l'avis", original_exception=e)

async def get_opinion(db: AsyncSession, opinion_id: int):
    """Récupère un avis par son ID."""
    try:
        stmt = select(models.Opinion).where(models.Opinion.id == opinion_id)
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
    except SQLAlchemyError as e:
        raise DALException(f"Erreur lors de la récupération de l'avis {opinion_id}", original_exception=e)

async def delete_opinion_by_id(db: AsyncSession, opinion_id: int):
    """Supprime un avis de la base de données."""
    try:
        db_opinion = await get_opinion(db, opinion_id)
        if db_opinion:
            await db.delete(db_opinion)
            await db.commit()
        return db_opinion
    except SQLAlchemyError as e:
        await db.rollback()  # IMPORTANT: annuler la transaction en cas d'erreur
        raise DALException(f"Erreur lors de la suppression de l'avis {opinion_id}", original_exception=e)

async def delete_opinion(db: AsyncSession, db_opinion: models.Opinion):
    """Supprime un avis de la base de données."""
    try:
        if db_opinion:
            await db.delete(db_opinion)
            await db.commit()
    except SQLAlchemyError as e:
        await db.rollback()  # IMPORTANT: annuler la transaction en cas d'erreur
        raise DALException(f"Erreur lors de la suppression de l'avis {db_opinion.id}", original_exception=e)
