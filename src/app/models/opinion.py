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