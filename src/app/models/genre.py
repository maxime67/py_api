from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from .base_class import Base

class Genre(Base):
    __tablename__ = "genres"
    id: Mapped[int] = mapped_column(primary_key=True)
    label: Mapped[str] = mapped_column(String(255))