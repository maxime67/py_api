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