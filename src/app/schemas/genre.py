from pydantic import BaseModel, ConfigDict

class GenreBase(BaseModel):
    label: str


class GenreCreate(GenreBase):
    pass


class GenreRead(GenreBase):
    id: int
    model_config = ConfigDict(from_attributes=True)