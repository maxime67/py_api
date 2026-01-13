from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.schemas.participant import ParticipantRead, ParticipantCreate, ParticipantUpdate
from app.services import participant as participant_service

router = APIRouter()

# ... existing code ...
@router.get("/participants/", response_model=List[ParticipantRead])
async def read_participants(db: AsyncSession = Depends(get_db)):
    """Récupère une liste de tous les participants."""
    return await participant_service.get_participants(db=db)

@router.post("/participants/", response_model=ParticipantRead, status_code=status.HTTP_201_CREATED)
async def create_participant(
    participant: ParticipantCreate, db: AsyncSession = Depends(get_db)
):
    """Crée un nouveau participant (acteur ou réalisateur)."""
    return await participant_service.create_participant(db=db, participant=participant)


@router.patch("/participants/{participant_id}", response_model=ParticipantRead)
async def update_participant(
    participant_id: int, participant_data: ParticipantUpdate, db: AsyncSession = Depends(get_db)
):
    """Met à jour un participant existant."""
    return await participant_service.update_participant(db=db, participant_id=participant_id, participant_data=participant_data)