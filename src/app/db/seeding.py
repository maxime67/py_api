from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.genre import Genre
from app.models.participant import Participant
from app.models.member import Member
from app.models.movie import Movie
from app.models.opinion import Opinion


async def seed_db(session: AsyncSession):
    """
    Préremplit la base de données avec des données initiales si elle est vide.
    """

    # 1. Vérifier si la BDD est déja remplie (ex: en comptant les genres)
    result = await session.execute(select(Genre))
    if result.scalars().first() is not None:
        print("La base de données contient déja des données. Seeding annulé.")
        return

    print("Base de données vide. Début du seeding...")

    # 2. Créer les Genres
    genre1 = Genre(label="Science-Fiction")
    genre2 = Genre(label="Comédie")
    genre3 = Genre(label="Drame")
    session.add_all([genre1, genre2, genre3])
    await session.commit()  # Commit pour que les objets aient un ID

    # 3. Créer les Participants (Acteurs/Réalisateurs)
    director1 = Participant(first_name="Christopher", last_name="Nolan")
    actor1 = Participant(first_name="Leonardo", last_name="DiCaprio")
    actor2 = Participant(first_name="Marion", last_name="Cotillard")
    session.add_all([director1, actor1, actor2])
    await session.commit()

    # 4. Créer un Membre
    member1 = Member(
        login="testuser",
        password="hashed_password_here",  # En réalité, il faudrait hasher ce mot de passe
        is_admin=False,
        first_name="Test",
        last_name="User"
    )
    session.add(member1)
    await session.commit()

    # 5. Créer un Film
    movie1 = Movie(
        title="Inception",
        year=2010,
        duration=148,
        synopsis="Un voleur qui s'approprie des secrets... (etc)",
        director_id=director1.id,
        genre_id=genre1.id,
        actors=[actor1, actor2]  # La relation M2M est gérée par SQLAlchemy
    )
    session.add(movie1)
    await session.commit()

    # 6. Créer un Avis
    opinion1 = Opinion(
        note=5,
        comment="Incroyable !",
        member_id=member1.id,
        movie_id=movie1.id
    )
    session.add(opinion1)
    await session.commit()

    print(f"Film '{movie1.title}' et ses relations ont été ajoutés.")
