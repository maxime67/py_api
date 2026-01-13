from pydantic import BaseModel, ConfigDict

from app.schemas.member import MemberRead

class OpinionBase(BaseModel):
    note: int
    comment: str


class OpinionCreate(OpinionBase):
    member_id: int


class OpinionRead(OpinionBase):
    id: int
    movie_id: int
    member: MemberRead
    model_config = ConfigDict(from_attributes=True)
