from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
import app.schemas.genre as genre_schemas
from app.api.deps import get_db
import app.services.genre as genre_service

router = APIRouter()

@router.get("/genres/", response_model=List[genre_schemas.GenreRead])
async def read_genres(db: AsyncSession = Depends(get_db)):
    """Récupère une liste de genres."""
    return await genre_service.get_genres(db=db)
