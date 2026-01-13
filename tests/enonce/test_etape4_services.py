import pytest
from unittest.mock import AsyncMock, patch

from app.services import genre as genre_service
from app.services import participant as participant_service
from app.services import opinion as opinion_service
from app.schemas.participant import ParticipantUpdate
from app.schemas.opinion import OpinionCreate
from app.core.exceptions import NotFoundBLLException, ValidationBLLException

# Marqueur pour indiquer à pytest que ce sont des tests asynchrones
pytestmark = pytest.mark.asyncio


async def test_get_genres_service(mocker):
    """Teste le TODO 'get_genres' (service) - Étape 4."""
    # 1. Arrange
    # Simuler le repository pour qu'il retourne une liste
    mock_repo = mocker.patch("app.repositories.genre.get_genres", new_callable=AsyncMock)
    mock_repo.return_value = [{"id": 1, "label": "Action"}]

    # 2. Act
    result = await genre_service.get_genres(db=AsyncMock())

    # 3. Assert
    mock_repo.assert_called_once()
    assert len(result) == 1
    assert result[0]["label"] == "Action"


async def test_update_participant_not_found(mocker):
    """Teste que update_participant (service) lève NotFoundBLLException - Étape 4."""
    # 1. Arrange
    # Simuler le repository pour qu'il retourne None
    mock_repo = mocker.patch("app.repositories.participant.update_participant", new_callable=AsyncMock)
    mock_repo.return_value = None

    update_data = ParticipantUpdate(first_name="Test")

    # 2. Act & 3. Assert
    with pytest.raises(NotFoundBLLException, match="Participant avec l'ID '999' non trouvé"):
        await participant_service.update_participant(
            db=AsyncMock(),
            participant_id=999,
            participant_data=update_data
        )


async def test_create_opinion_service_validation(mocker):
    """Teste la validation (note) dans create_opinion (service) - Étape 4."""
    # 1. Arrange
    # Simuler le service de film (nécessaire pour la validation)
    mocker.patch("app.services.movie.get_movie_by_id", new_callable=AsyncMock)
    # Simuler le service de membre (maintenant aussi nécessaire)
    mocker.patch("app.services.member.get_member_by_id", new_callable=AsyncMock)

    # Données d'opinion avec une note invalide
    opinion_data = OpinionCreate(note=10, comment="Trop haut!", member_id=1)

    # 2. Act & 3. Assert
    with pytest.raises(ValidationBLLException, match="La note doit être comprise entre 0 et 5"):
        await opinion_service.create_opinion(
            db=AsyncMock(),
            movie_id=1,
            opinion=opinion_data
        )


async def test_create_opinion_service_movie_not_found(mocker):
    """Teste que create_opinion lève NotFound si le film n'existe pas - Étape 4."""
    # 1. Arrange
    # Simuler le service de film pour qu'il lève l'exception
    mocker.patch(
        "app.services.movie.get_movie_by_id",
        new_callable=AsyncMock,
        side_effect=NotFoundBLLException(resource_name="Film", resource_id=999)
    )
    opinion_data = OpinionCreate(note=5, comment="Valide", member_id=1)

    # 2. Act & 3. Assert
    with pytest.raises(NotFoundBLLException, match="Film avec l'ID '999' non trouvé"):
        await opinion_service.create_opinion(
            db=AsyncMock(),
            movie_id=999,
            opinion=opinion_data
        )


async def test_delete_opinion_service_not_found(mocker):
    """Teste que delete_opinion (service) lève NotFound - Étape 4."""
    # 1. Arrange
    # Simuler le repository d'opinion pour qu'il retourne None
    mock_repo = mocker.patch("app.repositories.opinion.get_opinion", new_callable=AsyncMock)
    mock_repo.return_value = None

    # 2. Act & 3. Assert
    with pytest.raises(NotFoundBLLException, match="Avis avec l'ID '999' non trouvé"):
        await opinion_service.delete_opinion(db=AsyncMock(), opinion_id=999)