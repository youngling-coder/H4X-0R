from pydantic import BaseModel


class User(BaseModel):
    id: int
    reputation: float = 0.0
