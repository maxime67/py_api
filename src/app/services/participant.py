from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import participant as participant_repository
from app.schemas.participant import ParticipantCreate, ParticipantUpdate
from app.models.participant import Participant as ParticipantModel
from app.core.exceptions import NotFoundBLLException

async def get_participants(db: AsyncSession) -> List[ParticipantModel]:
    """Service pour récupérer une liste de participants."""
    return await participant_repository.get_participants(db)

async def create_participant(db: AsyncSession, participant: ParticipantCreate) -> ParticipantModel:
    """Service pour créer un nouveau participant."""
    return await participant_repository.create_participant(db, participant=participant)

async def update_participant(
    db: AsyncSession, participant_id: int, participant_data: ParticipantUpdate
) -> ParticipantModel:
    """Service pour mettre à jour un participant."""
    db_participant = await participant_repository.update_participant(db, participant_id, participant_data)
    if db_participant is None:
        raise NotFoundBLLException(resource_name="Participant", resource_id=participant_id)
    return db_participant
