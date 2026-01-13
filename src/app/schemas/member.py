from pydantic import BaseModel, ConfigDict

class MemberBase(BaseModel):
    login: str

class MemberRead(MemberBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
