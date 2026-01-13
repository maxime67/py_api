import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
# CORRECTION : Importer le modèle Movie
from app.models import Movie

# Marqueur pour indiquer à pytest que ce sont des tests asynchrones
pytestmark = pytest.mark.asyncio


async def test_read_genres_api(test_client: AsyncClient, test_data):
    """Teste le TODO 'GET /genres/' (API) - Étape 5."""
    response = await test_client.get("/api/v1/genres/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2  # "Science-Fiction" et "Action" de la fixture
    assert data[0]["label"] == "Science-Fiction"
    assert data[1]["label"] == "Action"


async def test_participants_api_workflow(test_client: AsyncClient, test_data):
    """
    Teste le workflow complet pour les participants :
    - POST /participants/ (TODO)
    - GET /participants/ (TODO)
    - PATCH /participants/{id} (TODO)
    """

    # 1. Tester GET /participants/ (TODO) avec les données de la fixture
    response_get_all = await test_client.get("/api/v1/participants/")
    assert response_get_all.status_code == 200
    list_data = response_get_all.json()
    assert len(list_data) == 2  # Nolan et DiCaprio

    # Utiliser les valeurs simples de la fixture test_data
    assert list_data[0]["last_name"] == test_data["actor_leo_lastname"]  # Trié par nom de famille
    assert list_data[1]["last_name"] == test_data["director_nolan_lastname"]

    # 2. Tester POST /participants/ (TODO)
    participant_data = {"first_name": "Greta", "last_name": "Gerwig"}
    response_post = await test_client.post("/api/v1/participants/", json=participant_data)

    assert response_post.status_code == 201
    created_data = response_post.json()
    assert created_data["first_name"] == "Greta"
    participant_id = created_data["id"]

    # 3. Tester PATCH /participants/{id} (TODO)
    patch_data = {"first_name": "G.", "last_name": "Gerwig-Baumbach"}
    response_patch = await test_client.patch(
        f"/api/v1/participants/{participant_id}",
        json=patch_data
    )
    assert response_patch.status_code == 200
    updated_data = response_patch.json()
    assert updated_data["first_name"] == "G."
    assert updated_data["last_name"] == "Gerwig-Baumbach"


async def test_opinions_api_workflow(test_client: AsyncClient, db_session: AsyncSession, test_data):
    """
    Teste le workflow des avis :
    - POST /movies/{id}/opinions/ (TODO)
    - DELETE /opinions/{id} (déjà fourni, mais on teste)
    """

    # 1. Créer un film de test manuellement pour avoir un movie_id

    # Ajouter les champs NOT NULL (duration, synopsis)
    movie = Movie(
        title="Inception",
        year=2010,
        duration=148,
        synopsis="Un film sur les rêves.",

        # Utiliser les ID simples de la fixture test_data
        genre_id=test_data["genre_action_id"],
        director_id=test_data["director_nolan_id"]
    )

    db_session.add(movie)
    await db_session.commit()
    await db_session.refresh(movie)
    movie_id = movie.id

    # 2. Tester POST /movies/{id}/opinions/ (TODO)
    opinion_data = {
        "note": 5,
        "comment": "Mind-blowing!",
        "member_id": test_data["member_user_id"]
    }
    response_post = await test_client.post(
        f"/api/v1/movies/{movie_id}/opinions/",
        json=opinion_data
    )

    assert response_post.status_code == 201
    created_opinion = response_post.json()
    assert created_opinion["comment"] == "Mind-blowing!"
    assert created_opinion["member"]["login"] == test_data["member_user_login"]

    opinion_id = created_opinion["id"]

    # 3. Tester DELETE /opinions/{id}
    response_delete = await test_client.delete(f"/api/v1/opinions/{opinion_id}")
    assert response_delete.status_code == 204  # No Content

    # 4. Vérifier que la suppression lève un 404 si on réessaye
    response_delete_again = await test_client.delete(f"/api/v1/opinions/{opinion_id}")
    assert response_delete_again.status_code == 404