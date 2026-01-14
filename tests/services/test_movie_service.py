import pytest
from unittest.mock import AsyncMock

from app.services import movie as movie_service
from app.schemas.movie import MovieCreate
from app.core.exceptions import NotFoundBLLException, ValidationBLLException

# Marqueur pour indiquer à pytest que ce sont des tests asynchrones
pytestmark = pytest.mark.asyncio


async def test_get_movie_by_id_success(mocker):
    """
    Vérifie que le service retourne un film si le repositories le trouve.
    """
    # 1. Préparation (Arrange)
    # On simule le repositories movie
    mock_repo = mocker.patch("app.repositories.movie.get_movie", new_callable=AsyncMock)

    # On configure le mock pour qu'il retourne une fausse donnée
    fake_movie_id = 1
    mock_repo.return_value = {"id": fake_movie_id, "title": "Fake Movie"}

    # 2. Action (Act)
    # On appelle la fonction du service à tester
    result = await movie_service.get_movie_by_id(db=AsyncMock(), movie_id=fake_movie_id)

    # 3. Assertion (Assert)
    # On vérifie que le service a bien appelé le repositories
    mock_repo.assert_called_once_with(mocker.ANY, movie_id=fake_movie_id)

    # On vérifie que le résultat est correct
    assert result["id"] == fake_movie_id


async def test_get_movie_by_id_not_found(mocker):
    """
    Vérifie que le service lève une exception NotFoundError si le repositories ne trouve rien.
    """
    # 1. Arrange
    # On simule le repositories pour qu'il retourne None
    mock_repo = AsyncMock(return_value=None)
    mocker.patch("app.repositories.movie.get_movie", new=mock_repo)

    # 2. Act & 3. Assert
    # On s'attend à ce qu'une exception soit levée et on vérifie son type
    with pytest.raises(NotFoundBLLException):
        await movie_service.get_movie_by_id(db=AsyncMock(), movie_id=999)


async def test_create_movie_invalid_year(mocker):
    """
    Vérifie que le service lève une ValidationError pour une année invalide.
    """
    # 1. Arrange
    movie_data = MovieCreate(title="The Future Movie", year=3000, genre_id=1, director_id=1)

    # Mock the repository to ensure we never reach it
    mock_repo = mocker.patch("app.repositories.movie.create_movie", new_callable=AsyncMock)

    # 2. Act & 3. Assert
    with pytest.raises(ValidationBLLException, match="L'année du film doit être comprise entre"):
        await movie_service.create_movie(db=AsyncMock(), movie=movie_data)

    # Verify the repository was never called (validation should happen before)
    mock_repo.assert_not_called()


async def test_create_movie_empty_title():
    """
    Vérifie que le service lève une ValidationError pour un titre vide.
    """
    # 1. Arrange
    movie_data = MovieCreate(title="  ", year=2020, genre_id=1, director_id=1)

    # 2. Act & 3. Assert
    with pytest.raises(ValidationBLLException, match="Le titre du film ne peut pas être vide."):
        await movie_service.create_movie(db=AsyncMock(), movie=movie_data)
