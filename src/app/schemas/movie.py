from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from .person import PersonRead
from .genre import GenreRead
from .opinion import OpinionRead

class MovieBase(BaseModel):
    title: str
    year: int
    duration: Optional[int] = None
    synopsis: Optional[str] = None


# Schéma pour la création : on utilise les IDs pour les relations
class MovieCreate(MovieBase):
    genre_id: int
    director_id: int
    actors_ids: List[int] = []


# Schéma complet pour la lecture : on imbrique les objets complets
class MovieRead(MovieBase):
    id: int
    genre: GenreRead
    director: PersonRead
    actors: List[PersonRead] = []
    opinions: List[OpinionRead] = []

    model_config = ConfigDict(from_attributes=True)