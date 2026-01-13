# TP : Filmothèque (API REST)

## Informations générales

**Cours** : Python Avancé > REST API > Fast API \
**Objectifs pédagogiques** :
- Créer une application backend basée sur FastAPI.
- Structurer une application en couches (API/Routeurs, BLL/Services, DAL/Repository).
- Définir des schémas de données avec Pydantic pour la validation et la sérialisation.
- Interagir avec une base de données en asynchrone grâce à SQLAlchemy.
- Mettre en place un système d'injection de dépendances (pour la session BDD).
- Gérer les erreurs de manière centralisée avec des gestionnaires d'exceptions personnalisés, en particulier pour DAL et BLL
- Tests : pytest
- Outils modernes et performants (uv, PyCharm, FastAPI, SQLAlchemy 2.x)
- Bonnes pratiques de l'entreprise

---

## Prérequis

### Connaissances préalables

  * Connaissances de base en programmation.
  * Application du modèle en couches (API, BLL, DAL).

### Architecture en couches

La pile applicative que nous allons construire suit une séparation claire des responsabilités :

```mermaid
graph TD
    A[API / Routeurs] -- "Appelle le" --> B[Services / BLL];
    B -- "Appelle le" --> C[Repository / DAL];
    C -- "Utilise l'" --> D[ORM / SQLAlchemy];
    D -- "Dialogue avec la" --> E[Base de donnees];
```

  * **API / Routeurs** : la porte d'entrée HTTP.
  * **Services / BLL** : la logique métier (Business Logic Layer).
  * **Repository / DAL** : l'abstraction de la persistance (Data Access Layer).
  * **ORM / SQLAlchemy** : les modèles et la session qui parlent à la BDD.

### Installation et configuration de l’environnement

- Installation des dépendances : faire `uv sync` (fichier lock déja présent)
- À ce stade, si vos imports ne sont pas reconnus dans l'IDE PyCharm à l'ouverture d'un fichier (par exemple `app/main.py`), marquer le répertoire `src` comme `Sources Root` (Clic droit sur répertoire `src`, puis `Mark Directory as ... > Sources Root`), puis redémarrer l'IDE (File > Invalidate Caches... > "Just restart" à gauche).
- Par défaut, vous travaillerez avec une base de données locale `sqlite`. C'est fortement recommandé pour gagner du temps !

### Lancement du projet

Une fois le projet cloné, se positionner dans le répertoire racine du projet (là où se trouve le fichier `pyproject.toml`).

Faire clic droit puis `Settings` sur l'onglet du terminal local Pycharm, puis définir la variable d'environnement `BACKEND_CORS_ORIGINS`, en prévision de l'accès à ce micro service depuis un front Angular :
- `BACKEND_CORS_ORIGINS=["http://localhost:4200"]`)

**À la fin du TP**, vous pourrez lancer le serveur, en ouvrant un (nouvel onglet) terminal local Pycharm, puis en lancant les commandes suivantes :

- `cd src`
- `uv run uvicorn app.main:app --host 0.0.0.0 --port 8000` (notez que l'option `--reload` de rechargement automatique du serveur est omise sous Windows, car elle peut rendre bloquant le terminal PyCharm)

Les URLs suivantes devront alors être accessibles, selon vos avancées sur le projet :

- http://127.0.0.1:8000/ -> retourne "welcome to this fantastic API"
- http://127.0.0.1:8000/api/v1/movies/ -> retourne une liste de films, éventuellement vide

Notez qu'un pré-remplissage de la base est possible via le fichier `app/db/seeding.py`.
Si vous souhaitez réinitialiser la base, vous pouvez supprimer le fichier `local_dev.db` à la racine de votre projet, en prenant soin de décocher l'option `safe delete` (pas de refactor nécessaire à cet effet).

---

## Énoncé

### Modèle logique : schéma UML

Vous trouverez ci-dessous pour information le schéma UML de la base de données.

![Modèle logique UML](./resources/tp_fastapi_uml.png)

**Note :** ce diagramme reflète les entités et les associations du **domaine métier**. L'implémentation technique réelle peut différer légèrement pour s'adapter aux contraintes du framework (par exemple : l'héritage de `BaseModel` pour les schémas Pydantic, la gestion explicite des clés étrangères dans SQLAlchemy, ou les tables d'association techniques).

### Structure du projet

La structure du projet `tp_fastapi` est la suivante :

```
tp_fastapi/
    src/
    ├── app/
    │   ├── api/
    │   │   ├── __init__.py
    │   │   ├── deps.py
    │   │   ├── exception_handlers.py
    │   │   └── routers/                  # la porte d'entrée HTTP
    │   │       ├── __init__.py
    │   │       ├── genres.py
    │   │       ├── movies.py
    │   │       ├── opinions.py
    │   │       └── participants.py
    │   ├── core/
    │   │   ├── __init__.py
    │   │   ├── config.py
    │   │   └── exceptions.py
    │   ├── db/
    │   │   ├── __init__.py
    │   │   └── session.py
    │   ├── models/                       # les Business Objects (BO), qui sont également des entités pour l'ORM SQLAlchemy
    │   │   ├── __init__.py
    │   │   ├── base_class.py
    │   │   ├── genre.py
    │   │   ├── member.py
    │   │   ├── movie.py
    │   │   ├── movie_actors.py
    │   │   ├── opinion.py
    │   │   ├── participant.py
    │   │   └── person.py
    │   ├── repository/                   # l'abstraction de la persistance (Data Access Layer)
    │   │   ├── __init__.py
    │   │   ├── genre.py
    │   │   ├── movie.py
    │   │   ├── opinion.py
    │   │   └── participant.py
    │   ├── schemas/                      # objets manipulés lors des requêtes/réponses HTTP 
    │   │   ├── __init__.py
    │   │   ├── genre.py
    │   │   ├── movie.py
    │   │   ├── opinion.py
    │   │   ├── participant.py
    │   │   └── person.py
    │   ├── services/                     # la logique métier (Business Logic Layer)
    │   │   ├── __init__.py
    │   │   ├── genre.py
    │   │   ├── movie.py
    │   │   ├── opinion.py
    │   │   └── participant.py
    │   ├── __init__.py
    │   └── main.py
```

### Note sur le typage : List vs Sequence

Nous utiliserons exclusivement le type `List` (importé de `typing` : `from typing import List`). Bien que `Sequence` soit souvent utilisé en Python pur pour les retours de lecture, ici `List` est impératif pour deux raisons :
- Avec SQLAlchemy, les relations (ex: actors) sont des collections mutables (modifiables) : on doit pouvoir y ajouter des éléments.
- Avec Pydantic et FastAPI, cela assure une sérialisation explicite en tableau JSON (Array).

## Étape 1 : les fondations - modèles de données ORM 

L'Object-Relational Mapping (ORM) est la couche qui traduit nos objets Python en tables de base de données.
C'est une partie importante, mais complexe.
Pour que vous puissiez vous concentrer sur l'architecture de l'API, **le code de ce répertoire `app/models/` vous est intégralement fourni**.

Votre mission est de **créer les fichiers et d'y copier le code ci-dessous**. Prenez le temps de lire et de comprendre les relations définies :
* `Person` est une classe de base utilisant l'**héritage** pour définir `Participant` (acteur/réalisateur) et `Member` (utilisateur).
* `Movie` a une relation **One-to-Many** avec `Opinion` (un film peut avoir plusieurs avis).
* `Movie` a une relation **Many-to-One** avec `Genre` et `Participant` (pour le réalisateur).
* `Movie` et `Participant` (pour les acteurs) ont une relation **Many-to-Many** via une table d'association.

#### Fichier : `app/models/base_class.py`
```python
from sqlalchemy.orm import declarative_base
Base = declarative_base()
```

#### Fichier : `app/models/person.py`
```python
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from .base_class import Base

class Person(Base):
    __tablename__ = "persons"
    id: Mapped[int] = mapped_column(primary_key=True)
    last_name: Mapped[str] = mapped_column(String(255))
    first_name: Mapped[str] = mapped_column(String(255))
    # colonne discriminante pour la hiérarchie d'héritage
    type: Mapped[str] = mapped_column(String(50))

    __mapper_args__ = {
        "polymorphic_identity": "person",
        "polymorphic_on": "type",
    }
```

#### Fichier : `app/models/participant.py`
```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .person import Person

class Participant(Person):
    __tablename__ = "participants"
    id: Mapped[int] = mapped_column(ForeignKey("persons.id"), primary_key=True)
    __mapper_args__ = {"polymorphic_identity": "participant"}
```

#### Fichier : `app/models/genre.py`
```python
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from .base_class import Base

class Genre(Base):
    __tablename__ = "genres"
    id: Mapped[int] = mapped_column(primary_key=True)
    label: Mapped[str] = mapped_column(String(255))
```

#### Fichier : `app/models/movie_actors.py`
```python
from sqlalchemy import Column, ForeignKey, Table
from .base_class import Base

movie_actors_association_table = Table(
    "movie_actors_association",
    Base.metadata,
    Column("movie_id", ForeignKey("movies.id"), primary_key=True),
    Column("participant_id", ForeignKey("participants.id"), primary_key=True),
)
```

#### Fichier : `app/models/movie.py`
```python
from sqlalchemy import Integer, String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from .base_class import Base
from .movie_actors import movie_actors_association_table

class Movie(Base):
    __tablename__ = "movies"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    year: Mapped[int] = mapped_column(Integer)
    duration: Mapped[int] = mapped_column(Integer)
    synopsis: Mapped[str] = mapped_column(Text)
    director_id: Mapped[int] = mapped_column(ForeignKey("participants.id"))
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.id"))

    director: Mapped["Participant"] = relationship(foreign_keys=[director_id])
    genre: Mapped["Genre"] = relationship()
    actors: Mapped[List["Participant"]] = relationship(secondary=movie_actors_association_table)
    opinions: Mapped[List["Opinion"]] = relationship(back_populates="movie", cascade="all, delete-orphan")
```

#### Fichier : `app/models/opinion.py`

```python
from sqlalchemy import (
    Integer,
    ForeignKey,
    Text
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)
from .base_class import Base

class Opinion(Base):
    __tablename__ = "opinions"
    id: Mapped[int] = mapped_column(primary_key=True)
    note: Mapped[int] = mapped_column(Integer)
    comment: Mapped[str] = mapped_column(Text)

    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"))
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"))

    member: Mapped["Member"] = relationship(back_populates="opinions")
    movie: Mapped["Movie"] = relationship(back_populates="opinions")
```

#### Fichier : `app/models/member.py`

```python
from sqlalchemy import (
    String,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)
from typing import List
from .person import Person

class Member(Person):
    __tablename__ = "members"

    # La clé primaire est aussi une clé étrangère vers la table parente
    id: Mapped[int] = mapped_column(ForeignKey("persons.id"), primary_key=True)

    # Champs spécifiques à Member
    login: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    # La relation vers Opinion
    opinions: Mapped[List["Opinion"]] = relationship(back_populates="member")

    __mapper_args__ = {
        "polymorphic_identity": "member",
    }

    def __repr__(self) -> str:
        return f"Member(id={self.id}, login='{self.login}')"
```

#### Fichier : `app/models/__init__.py`

Pensez également à **importer toutes les classes dans `app/models/__init__.py`** pour faciliter les imports ailleurs dans le projet :

```python
# app/models/__init__.py

# Eviter les erreurs liés à l'importation circulaire
# Exemple : sqlalchemy.exc.InvalidRequestError: When initializing mapper Mapper[Movie(movies)], expression 'Genre' failed to locate a name ('Genre'). If this is a class name, consider adding this relationship() to the <class 'app.models.film.Film'> class after both dependent classes have been defined

from .base_class import Base
from .genre import Genre
from .member import Member
from .movie import Movie
from .opinion import Opinion
from .participant import Participant
from .person import Person

# L'import des associations (ex : personnefilm) n'est en général pas nécessaire ici car elles sont gérées dans les modèles eux-mêmes
```

---

## Étape 2 : les schémas de données avec Pydantic

Les schémas Pydantic définissent la "forme" des données que notre API attend en entrée et renvoie en sortie. Ils assurent une validation robuste et automatique.

Votre mission : **Créez les fichiers dans `app/schemas/`** et écrivez les classes Pydantic. Une bonne pratique est de créer :
* Une classe `Base` (champs communs).
* Une classe `Create` (champs requis pour la création).
* Une classe `Read` (pour la lecture, avec les `id` et les relations).

**Exemple pour `genre.py` :**
```python
from pydantic import BaseModel, ConfigDict

class GenreBase(BaseModel):
    label: str

class GenreCreate(GenreBase):
    pass

class GenreRead(GenreBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
```
Inspirez-vous de cet exemple et des modèles ORM pour créer les schémas pour `Person`, `Participant`, `Opinion` et `Movie`.

**Astuce pour `Movie` :** Le schéma de création `MovieCreate` attendra des IDs (`director_id`, `actors_ids`), tandis que le schéma de lecture `MovieRead` renverra les objets imbriqués (`director: Person`, `actors: List[Person]`).

Pour valider votre travail, vous pouvez lancer le test suivant, à la racine du projet : `uv run pytest tests/enonce/test_etape2_schemas.py`.

---

## Étape 3 : la couche d'accès aux données (DAL / Repository)

Dans la couche DAL (Data Access Layer), le Repository est responsable de toutes les requêtes à la base de données. C'est ici que vous écrirez vos requêtes SQLAlchemy. L'objectif est de cacher la complexité de l'ORM au reste de l'application.

Votre mission : **Complétez les fonctions dans les fichiers du répertoire `app/repositories/`**.
Toutes les fonctions recevront une session `db: AsyncSession` en paramètre.

**Exemple pour `repositories\movie.py` :**
* **`get_movie(db, movie_id)`** : Doit récupérer un film par son ID. Pensez à utiliser `selectinload` pour charger ses relations (genre, réalisateur, acteurs) de manière efficace et éviter le problème N+1.
* **`get_movies(db, skip, limit)`** : Récupère une liste de films paginée.
* **`create_movie(db, movie)`** : Crée une nouvelle instance `Movie`, l'ajoute à la session et la commit.

**Important** : entourez vos requêtes d'un bloc `try...except SQLAlchemyError` et levez une `DALException` personnalisée en cas d'erreur.

Pour valider votre travail, vous pouvez lancer le test suivant, à la racine du projet : `uv run pytest tests/enonce/test_etape3_repositories.py`.

---

## Étape 4 : la logique métier (BLL / Services)

Le Service est le cœur de votre logique. Il orchestre les appels au Repository et applique les règles métier. C'est lui qui décide si une action est valide ou non.

Votre mission : **Implémentez la logique dans les fichiers du répertoire `app/services/`**.

**Exemple pour `services\movie.py` :**
* Dans `create_movie`, avant d'appeler le repository, **ajoutez des vérifications** :
    1.  Le titre du film ne doit pas être vide.
    2.  L'année de sortie doit être réaliste (ex: entre 1888 et aujourd'hui + 5 ans).
    3.  Si une de ces règles n'est pas respectée, levez une `ValidationBLLException`.
* Dans `get_movie_by_id`, si le repository ne retourne aucun film, levez une `NotFoundBLLException`.

**Principe clé** : Un service ne doit jamais manipuler directement des exceptions HTTP (`HTTPException`). Il utilise des exceptions métier personnalisées (`BLLException`, `NotFoundBLLException`, etc.) pour rester indépendant du framework web.

Pour valider votre travail, vous pouvez lancer le test suivant, à la racine du projet : `uv run pytest tests/enonce/test_etape4_services.py`.

---

## Étape 5 : la couche API (Routers)

C'est ici que tout se connecte ! Les routeurs FastAPI définissent les endpoints de votre API, reçoivent les requêtes HTTP, appellent les services appropriés et retournent les réponses.

Votre mission : **Créez les endpoints dans les fichiers du répertoire `app/api/routers/`**.

* Utilisez les décorateurs de FastAPI (`@router.get`, `@router.post`, etc.).
* Utilisez `response_model` pour spécifier le schéma Pydantic de la réponse.
* Utilisez `status_code` pour définir le code de statut HTTP approprié (ex: `201 CREATED`).
* Injectez la session de base de données en utilisant `db: AsyncSession = Depends(get_db)`.
* Appelez la fonction de service correspondante et retournez son résultat.

Pour que vos endpoints soient accessibles, pensez à les déclarer immédiatement dans `app/main.py` avec `app.include_router(...)` dès que vous créez un fichier routeur.

Pour valider votre travail, vous pouvez lancer le test suivant, à la racine du projet : `uv run pytest tests/enonce/test_etape5_api.py`.

---

## Étape 6 : l'assemblage final et la gestion des erreurs

La dernière étape consiste à configurer l'application FastAPI principale, à connecter les routeurs et à mettre en place la gestion centralisée des exceptions.

Votre mission : **Complétez le fichier `app/main.py` et observez `app/api/exception_handlers.py`**.

1.  Dans `main.py` :
    * Créez l'instance `FastAPI`, si ce n'est pas déja fait.
    * Utilisez `app.include_router()` pour ajouter chaque routeur que vous avez créé (normalement fait à l'étape 5).
    * Utilisez `@app.add_exception_handler()` pour lier vos exceptions métier personnalisées (`NotFoundBLLException`, `ValidationBLLException`, `DALException`, `BLLException`) à des fonctions de gestion.

2.  Dans `app/api/exception_handlers.py`, observez les points suivants :
    * Les fonctions `async def` (ex: `not_found_bll_exception_handler`) qui prennent `Request` et votre exception en paramètres. À quoi servent-elles ?
    * Ces fonctions doivent retourner une `JSONResponse` avec le code de statut HTTP adéquat (`404`, `400`, `500`) et un message d'erreur clair dans le contenu. Pourquoi c'est une bonne pratique avec REST de retourner un code status HTTP approprié ? Est-ce que le code en question sépare les erreurs techniques des erreurs fonctionnelles ?

Le schéma ci-dessous illustre comment les exceptions personnalisées sont levées par les couches internes (DAL, BLL) et interceptées par les gestionnaires centraux (handlers) définis dans `main.py` pour produire une réponse HTTP propre.

```mermaid
graph TD
    subgraph "Flux de requete"
        A[Requete HTTP] --> B[Endpoint API]
        B -- Appelle --> C(Service BLL)
        C -- Appelle --> D(Repository DAL)
    end

    subgraph "Flux d'exception"
        D -- Leve --> E{DALException}
        C -- Leve --> F{NotFoundBLLException}
        C -- Leve --> G{ValidationBLLException}

        H[main.py: @app.add_exception_handler] -- Enregistre --> I(handler_dal)
        H -- Enregistre --> J(handler_not_found)
        H -- Enregistre --> K(handler_validation)

        E -.-> I
        F -.-> J
        G -.-> K

        I -- Genere --> L[JSONResponse 500]
        J -- Genere --> M[JSONResponse 404]
        K -- Genere --> N[JSONResponse 400]
    end
```

Une fois terminé, lancez votre application avec `uv run uvicorn app.main:app --reload` (depuis le dossier `src/`) et explorez la documentation interactive sur `http://127.0.0.1:8000/docs`.

-----

## Aller plus loin (bonus)

* Vérifier que l'intégralité des tests passent. Se positionner à la racine du projet (avant le src), puis lancer les tests unitaires via :
   - `uv run pytest`
   - `uv run pytest -vv` (avec davantage d'éléments de debug)
* Implémentez-les endpoints `UPDATE` et `DELETE` pour les participants et les films.
* Ajoutez des filtres à la route `GET /movies/` (par année, par genre, etc.).
* Lancer les tests unitaires suivants : `uv run pytest tests/api/test_movies_api.py` et `uv run pytest tests/services/test_movie_service.py`
* Écrivez d'autres tests unitaires et d'intégration avec `pytest`.
* Mettre en œuvre une véritable base de données MySQL :

Si vous souhaitez établir une connexion avec une véritable base de données telle que MySQL, sachez que le package `asyncmy` sera requis (`uv add "asyncmy>=0.2.10"`), ainsi qu'au préalable sous Windows, l'installation des redistributables Visual Studio 2022 (via l'outil vsBuildTools dont le binaire et la documentation sont transmis dans votre `00_Install_Pack.zip`).

```
La base doit être créée au préalable (exemple en root) :

CREATE DATABASE filmotheque CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

Un utilisateur filmotheque (mdp : filmotheque) doit être créé avec les droits sur cette base.
```

Faire clic droit puis Settings sur l'onglet du terminal local Pycharm, puis définir la variable d'environnement DATABASE_URL, contenant l'URL de connexion MySQL adéquate :

`DATABASE_URL=mysql+asyncmy://filmotheque:filmotheque@127.0.0.1:3306/filmotheque`

Fermez l'onglet du terminal, puis en ouvrir un autre, afin que les modifications soient effectives