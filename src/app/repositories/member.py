from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.member import Member
from sqlalchemy.exc import SQLAlchemyError
from app.core.exceptions import DALException

async def get_member(db: AsyncSession, member_id: int):
    """Récupère un membre par son ID."""
    try:
        result = await db.execute(select(Member).where(Member.id == member_id))
        return result.scalar_one_or_none()
    except SQLAlchemyError as e:
        raise DALException(f"Erreur lors de la récupération du membre {member_id}", original_exception=e)
