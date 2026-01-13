from pydantic import BaseModel, ConfigDict
from typing import Optional

class PersonBase(BaseModel):
    last_name: str
    first_name: Optional[str] = None


class PersonCreate(PersonBase):
    pass


class PersonRead(PersonBase):
    id: int
    model_config = ConfigDict(from_attributes=True)