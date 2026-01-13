import pytest
import pytest_asyncio
from typing import AsyncGenerator
import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.api.deps import get_db
from app.models import Base, Genre, Participant, Member

# URL pour une base de données SQLite en mémoire
TEST_DATABASE_URL = "sqlite+aiosqlite:///file:memdb_tp_filmotheque?mode=memory&cache=shared"

# Créer un moteur de BDD de test
engine = create_async_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Fixture pour fournir une session de BDD de test isolée pour chaque test.
    Recrée les tables à chaque fois pour garantir un état propre.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as session:
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()


@pytest.fixture(scope="function")
def override_get_db(db_session: AsyncSession):
    """Fixture pour surcharger la dépendance get_db de l'application."""

    async def _override_get_db():
        yield db_session

    return _override_get_db


@pytest_asyncio.fixture(scope="function")
async def test_client(override_get_db) -> AsyncGenerator[AsyncClient, None]:
    """Fixture pour le client HTTP de FastAPI."""
    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="function")
async def test_data(db_session: AsyncSession):
    """
    Fixture pour insérer des données de test initiales.
    """
    # 1. Créer les objets
    genre_sf = Genre(label="Science-Fiction")
    genre_action = Genre(label="Action")
    director_nolan = Participant(first_name="Christopher", last_name="Nolan")
    actor_leo = Participant(first_name="Leonardo", last_name="DiCaprio")

    member_user = Member(
        first_name="Test",
        last_name="User",
        login="testuser",
        password="password",
        is_admin=False
    )

    db_session.add_all([genre_sf, genre_action, director_nolan, actor_leo, member_user])
    await db_session.commit()

    # Rafraîchir les objets après le commit pour charger leurs ID
    await db_session.refresh(genre_sf)
    await db_session.refresh(genre_action)
    await db_session.refresh(director_nolan)
    await db_session.refresh(actor_leo)
    await db_session.refresh(member_user)

    # --- CORRECTION FINALE ---
    # Ne pas retourner les objets SQLAlchemy eux-mêmes, mais seulement leurs ID
    # et les valeurs simples.
    return {
        "genre_sf_id": genre_sf.id,
        "genre_action_id": genre_action.id,
        "director_nolan_id": director_nolan.id,
        "director_nolan_lastname": director_nolan.last_name,
        "actor_leo_id": actor_leo.id,
        "actor_leo_lastname": actor_leo.last_name,
        "member_user_id": member_user.id,
        "member_user_login": member_user.login
    }