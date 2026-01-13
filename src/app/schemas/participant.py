from pydantic import BaseModel, ConfigDict
from typing import Optional
from .person import PersonBase

class ParticipantCreate(PersonBase):
    pass


class ParticipantUpdate(BaseModel):
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    model_config = ConfigDict(extra="forbid")

class ParticipantRead(PersonBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
