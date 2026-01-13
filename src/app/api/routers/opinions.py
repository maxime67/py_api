from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import app.schemas.opinion as opinion_schemas
from app.api.deps import get_db
import app.services.opinion as opinion_service
from fastapi import Response, status

router = APIRouter()

@router.post("/movies/{movie_id}/opinions/", response_model=opinion_schemas.OpinionRead, status_code=status.HTTP_201_CREATED)
async def create_opinion_for_movie(
        movie_id: int, opinion: opinion_schemas.OpinionCreate, db: AsyncSession = Depends(get_db)
):
    """Ajoute un avis à un film spécifique."""
    return await opinion_service.create_opinion(db=db, movie_id=movie_id, opinion=opinion)

@router.delete("/opinions/{opinion_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_opinion(opinion_id: int, db: AsyncSession = Depends(get_db)):
    """Supprime un avis par son ID."""
    await opinion_service.delete_opinion(db=db, opinion_id=opinion_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
