from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
import app.schemas.movie as movie_schemas
from app.api.deps import get_db
import app.services.movie as movie_service
from fastapi import status

router = APIRouter()

@router.post("/movies/", response_model=movie_schemas.MovieRead, status_code=status.HTTP_201_CREATED)
async def create_movie(movie: movie_schemas.MovieCreate, db: AsyncSession = Depends(get_db)):
    """Crée un nouveau film."""
    return await movie_service.create_movie(db=db, movie=movie)

@router.get("/movies/", response_model=List[movie_schemas.MovieRead])
async def read_movies(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """Récupère une liste de films."""
    return await movie_service.get_movies(db=db, skip=skip, limit=limit)

@router.get("/movies/{movie_id}", response_model=movie_schemas.MovieRead)
async def read_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    """Récupère les détails d'un film spécifique par son ID."""
    return await movie_service.get_movie_by_id(db=db, movie_id=movie_id)
