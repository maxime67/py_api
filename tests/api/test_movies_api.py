import pytest
from httpx import AsyncClient

# Marqueur pour indiquer à pytest que ce sont des tests asynchrones
pytestmark = pytest.mark.asyncio


# Données de test réutilisables
@pytest.fixture
async def test_data(db_session):
    """Fixture pour insérer des données de test initiales."""
    from app.models import Genre, Participant

    # 1. Créer les objets
    genre = Genre(label="Science-Fiction")
    director = Participant(first_name="Denis", last_name="Villeneuve")

    db_session.add_all([genre, director])
    await db_session.commit()

    # 2. Rafraîchir les objets pour obtenir les ID générés par la BDD
    await db_session.refresh(genre)
    await db_session.refresh(director)

    # 3. Renvoyer uniquement les ID, pas les objets entiers
    return {"genre_id": genre.id, "director_id": director.id}


async def test_create_movie_success(test_client: AsyncClient, test_data):
    """Vérifie la création réussie d'un film via l'API."""
    response = await test_client.post(
        "/api/v1/movies/",
        json={
            "title": "Dune",
            "year": 2021,
            "duration": 155,
            "synopsis": "A mythic and emotionally charged hero's journey.",
            "genre_id": test_data["genre_id"],
            "director_id": test_data["director_id"],
            "actors_ids": []
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Dune"
    assert "id" in data
    assert data["genre"]["label"] == "Science-Fiction"


async def test_create_movie_validation_error(test_client: AsyncClient, test_data):
    """Vérifie que l'API retourne une erreur 400 pour des données invalides."""
    response = await test_client.post(
        "/api/v1/movies/",
        json={
            "title": "Future Movie",
            "year": 1800,  # Année invalide
            "genre_id": test_data["genre_id"],
            "director_id": test_data["director_id"],
        },
    )
    assert response.status_code == 400
    assert "L'année du film doit être comprise entre" in response.json()["detail"]


async def test_read_movie_not_found(test_client: AsyncClient):
    """Vérifie que l'API retourne une erreur 404 pour un film inexistant."""
    response = await test_client.get("/api/v1/movies/999")
    assert response.status_code == 404
    assert "Film avec l'ID '999' non trouvé." in response.json()["detail"]
