from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from .person import Person

class Participant(Person):
    __tablename__ = "participants"
    id: Mapped[int] = mapped_column(ForeignKey("persons.id"), primary_key=True)
    __mapper_args__ = {"polymorphic_identity": "participant"}