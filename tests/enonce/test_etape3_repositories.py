import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import movie as movie_repository
from app.repositories import opinion as opinion_repository
from app.repositories import genre as genre_repository
from app.schemas.movie import MovieCreate
from app.schemas.opinion import OpinionCreate
from app.models import Genre, Participant, Member, Movie, Opinion

# Marqueur pour indiquer à pytest que ce sont des tests asynchrones
pytestmark = pytest.mark.asyncio


@pytest.fixture
async def repo_test_data(db_session: AsyncSession):
    """Fixture pour insérer des données de test pour les tests de repository."""

    # 1. Créer tous les objets ORM manuellement
    genre = Genre(label="Science-Fiction")
    director = Participant(first_name="Denis", last_name="Villeneuve")
    member = Member(
        first_name="Repo",
        last_name="Tester",
        login="repo_user",
        password="pwd"
    )

    db_session.add_all([genre, director, member])
    await db_session.flush()

    # 2. Créer les objets dépendants (Movie, Opinion) manuellement

    # Ajouter des valeurs pour les champs NOT NULL (duration et synopsis)
    db_movie = Movie(
        title="Dune",
        year=2021,
        duration=155,
        synopsis="Un film sur le sable et les vers.",
        genre_id=genre.id,
        director_id=director.id
    )

    db_session.add(db_movie)
    await db_session.flush()  # Flusher pour obtenir l'ID du film

    db_opinion = Opinion(
        note=5,
        comment="Génial",
        member_id=member.id,
        movie_id=db_movie.id
    )
    db_session.add(db_opinion)

    # 3. Faire un SEUL commit à la fin pour tout sauvegarder
    await db_session.commit()

    # 4. Rafraîchir les objets pour être sûr qu'ils sont chargés pour les tests
    await db_session.refresh(genre)
    await db_session.refresh(director)
    await db_session.refresh(member)
    await db_session.refresh(db_movie)
    await db_session.refresh(db_opinion)

    # Rafraîchir aussi les relations du film
    await db_session.refresh(db_movie, attribute_names=["genre", "director", "opinions"])

    return {
        "movie": db_movie,
        "opinion": db_opinion,
        "genre": genre,
        "director": director,
        "member": member
    }


async def test_get_movies_repository(db_session: AsyncSession, repo_test_data):
    """Teste le TODO 'get_movies' dans movie_repository - Étape 3."""

    # 1. Appeler la fonction à tester
    movies = await movie_repository.get_movies(db_session, skip=0, limit=10)

    # 2. Vérifier les résultats
    assert isinstance(movies, list)
    assert len(movies) == 1
    assert movies[0].title == "Dune"
    # Vérifier que les relations sont chargées (problème N+1)
    assert movies[0].genre is not None
    assert movies[0].genre.label == "Science-Fiction"
    assert movies[0].director is not None
    assert movies[0].director.last_name == "Villeneuve"
    assert movies[0].opinions is not None
    assert len(movies[0].opinions) == 1
    assert movies[0].opinions[0].comment == "Génial"


async def test_get_delete_opinion_repository(db_session: AsyncSession, repo_test_data):
    """Teste les TODO 'get_opinion' et 'delete_opinion_by_id' - Étape 3."""

    opinion_id = repo_test_data["opinion"].id

    # 1. Tester get_opinion (TODO)
    fetched_opinion = await opinion_repository.get_opinion(db_session, opinion_id)
    assert fetched_opinion is not None
    assert fetched_opinion.id == opinion_id
    assert fetched_opinion.comment == "Génial"

    # 2. Tester delete_opinion_by_id (TODO)
    deleted_opinion = await opinion_repository.delete_opinion_by_id(db_session, opinion_id)
    assert deleted_opinion is not None
    assert deleted_opinion.id == opinion_id

    # 3. Vérifier que l'avis a bien été supprimé
    fetched_again = await opinion_repository.get_opinion(db_session, opinion_id)
    assert fetched_again is None


async def test_get_genres_repository(db_session: AsyncSession, repo_test_data):
    """Teste 'get_genres' (déjà implémenté, mais bon à avoir)."""
    genres = await genre_repository.get_genres(db_session)
    assert isinstance(genres, list)
    assert len(genres) >= 1
    assert genres[0].label == "Science-Fiction"