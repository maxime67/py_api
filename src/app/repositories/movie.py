from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError
from app.core.exceptions import DALException

from app.models.movie import Movie
from app.models.opinion import Opinion
import app.schemas.movie as schemas
import app.models.person as person_models

async def get_movie(db: AsyncSession, movie_id: int):
    """Récupère un film par son ID avec ses relations."""
    try:
        stmt = (
            select(Movie)
            .where(Movie.id == movie_id)
            .options(
                selectinload(Movie.genre),
                selectinload(Movie.director),
                selectinload(Movie.actors),
                selectinload(Movie.opinions),
                selectinload(Movie.opinions).selectinload(Opinion.member)
            )
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
    except SQLAlchemyError as e:
        raise DALException(f"Erreur lors de la récupération du film {movie_id}", original_exception=e)

async def get_movies(db: AsyncSession, skip: int = 0, limit: int = 100):
    """Récupère une liste de films avec leurs relations principales."""
    try:
        stmt = (
            select(Movie)
            .options(
                selectinload(Movie.genre),
                selectinload(Movie.director),
                selectinload(Movie.actors),
                selectinload(Movie.opinions),
                selectinload(Movie.opinions).selectinload(Opinion.member)
            )
            .order_by(Movie.title)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(stmt)
        return result.scalars().all()
    except SQLAlchemyError as e:
        raise DALException("Erreur lors de la récupération des films", original_exception=e)

async def create_movie(db: AsyncSession, movie: schemas.MovieCreate):
    """Crée un nouveau film."""
    try:
        # Récupérer les objets acteurs à partir de leurs IDs
        actors_result = await db.execute(
            select(person_models.Person).where(person_models.Person.id.in_(movie.actors_ids))
        )
        actors = actors_result.scalars().all()

        # Créer l'instance du film
        db_movie = Movie(
            title=movie.title,
            year=movie.year,
            duration=movie.duration,
            synopsis=movie.synopsis,
            genre_id=movie.genre_id,
            director_id=movie.director_id,
            actors=actors
        )
        db.add(db_movie)
        await db.commit()

        # Recharger les relations pour les retourner dans la réponse
        await db.refresh(db_movie)
        return await get_movie(db, db_movie.id)
    except SQLAlchemyError as e:
        await db.rollback() # IMPORTANT: annuler la transaction en cas d'erreur
        raise DALException("Erreur lors de la création du film", original_exception=e)
