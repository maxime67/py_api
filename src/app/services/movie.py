import datetime
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

import app.repositories.movie as movie_repository
import app.schemas.movie as movie_schemas
import app.models.movie as movie_models
from app.core.exceptions import NotFoundBLLException, ValidationBLLException

async def get_movies(db: AsyncSession, skip: int, limit: int) -> List[movie_models.Movie]:
    """Service pour récupérer une liste de films."""
    # Actuellement un simple relais, mais la logique complexe (filtres, etc.) irait ici.
    return await movie_repository.get_movies(db, skip=skip, limit=limit)

async def get_movie_by_id(db: AsyncSession, movie_id: int) -> movie_models.Movie:
    """Service pour récupérer un film par son ID."""
    db_movie = await movie_repository.get_movie(db, movie_id=movie_id)
    if db_movie is None:
        # Utiliser notre exception métier, pas une exception HTTP, pour des raisons de séparation des préoccupations.
        raise NotFoundBLLException(resource_name="Film", resource_id=movie_id)
    return db_movie

async def create_movie(db: AsyncSession, movie: movie_schemas.MovieCreate) -> movie_models.Movie:
    """Service pour créer un nouveau film."""

    if not movie.title or not movie.title.strip():
        raise ValidationBLLException("Le titre du film ne peut pas être vide.")

    current_year = datetime.datetime.now().year

    if 1888 <= movie.year <= current_year:
        return ValidationBLLException("L'année doit être cohérente")



    return await movie_repository.create_movie(db=db, movie=movie)

