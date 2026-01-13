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