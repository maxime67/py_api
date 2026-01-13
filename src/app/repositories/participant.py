from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.participant import Participant as ParticipantModel
from app.schemas.participant import ParticipantCreate, ParticipantUpdate
from sqlalchemy.exc import SQLAlchemyError
from app.core.exceptions import DALException


async def get_participant(db: AsyncSession, participant_id: int):
    """Récupère un participant par son ID."""
    try:
        result = await db.execute(select(ParticipantModel).where(ParticipantModel.id == participant_id))
        return result.scalar_one_or_none()
    except SQLAlchemyError as e:
        raise DALException(f"Erreur lors de la récupération du participant {participant_id}", original_exception=e)

async def get_participants(db: AsyncSession):
    """Récupère tous les participants de la base de données."""
    try:
        result = await db.execute(select(ParticipantModel).order_by(ParticipantModel.last_name))
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise DALException("Erreur lors de la récupération des participants", original_exception=e)

async def create_participant(db: AsyncSession, participant: ParticipantCreate) -> ParticipantModel:
    """Crée un nouveau participant."""
    try:
        db_participant = ParticipantModel(
            first_name=participant.first_name,
            last_name=participant.last_name
        )
        db.add(db_participant)
        await db.commit()
        await db.refresh(db_participant)
        return db_participant
    except SQLAlchemyError as e:
        await db.rollback()  # IMPORTANT: annuler la transaction en cas d'erreur
        raise DALException("Erreur lors de la création du participant", original_exception=e)

async def update_participant(
        db: AsyncSession, participant_id: int, participant_data: ParticipantUpdate
) -> ParticipantModel:
    """Met à jour les informations d'un participant existant."""
    try:
        db_participant = await get_participant(db, participant_id)
        if not db_participant:
            return None

        # Met à jour les champs si la valeur n'est pas None
        update_data = participant_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_participant, key, value)

        await db.commit()
        await db.refresh(db_participant)
        return db_participant
    except SQLAlchemyError as e:
        await db.rollback()
        raise DALException(f"Erreur lors de la mise à jour du participant {participant_id}", original_exception=e)

