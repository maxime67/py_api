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