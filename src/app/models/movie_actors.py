from sqlalchemy import Column, ForeignKey, Table
from .base_class import Base

movie_actors_association_table = Table(
    "movie_actors_association",
    Base.metadata,
    Column("movie_id", ForeignKey("movies.id"), primary_key=True),
    Column("participant_id", ForeignKey("participants.id"), primary_key=True),
)