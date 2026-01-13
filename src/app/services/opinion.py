from sqlalchemy.ext.asyncio import AsyncSession

import app.services.movie as movie_service
import app.services.member as member_service
import app.repositories.opinion as opinion_repository
import app.schemas.opinion as opinion_schemas
import app.models.opinion as opinion_models

from app.core.exceptions import NotFoundBLLException, ValidationBLLException

async def create_opinion(
        db: AsyncSession, *, movie_id: int, opinion: opinion_schemas.OpinionCreate
) -> opinion_models.Opinion:
    """
    Service pour créer un avis pour un film.
    Contient la logique métier : vérifier que le film existe et que la note est valide.
    """

    # Règle métier 1 : on ne peut pas noter un film qui n'existe pas.
    # On utilise le service movie qui lève déjà une NotFoundError propre.
    await movie_service.get_movie_by_id(db, movie_id=movie_id)

    # Règle métier 2 : l'auteur de l'avis (Membre) doit exister.
    await member_service.get_member_by_id(db, member_id=opinion.member_id)

    # Règle métier 3 : la note doit être dans un intervalle valide (ex: 0 à 5)
    if not (0 <= opinion.note <= 5):
        raise ValidationBLLException("La note doit être comprise entre 0 et 5.")

    # Appel au repositories pour la création pure
    return await opinion_repository.create_opinion_for_movie(db=db, opinion=opinion, movie_id=movie_id)


async def delete_opinion(db: AsyncSession, opinion_id: int) -> opinion_models.Opinion:
    """Service pour supprimer un avis."""
    db_opinion = await opinion_repository.get_opinion(db, opinion_id=opinion_id)
    if db_opinion is None:
        raise NotFoundBLLException(resource_name="Avis", resource_id=opinion_id)
    await opinion_repository.delete_opinion(db, db_opinion=db_opinion)
    return db_opinion
