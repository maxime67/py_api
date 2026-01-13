from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import member as member_repository
from app.models.member import Member as MemberModel
from app.core.exceptions import NotFoundBLLException

async def get_member_by_id(db: AsyncSession, member_id: int) -> MemberModel:
    """Service pour récupérer un membre par son ID."""
    db_member = await member_repository.get_member(db, member_id=member_id)
    if db_member is None:
        raise NotFoundBLLException(resource_name="Membre", resource_id=member_id)
    return db_member