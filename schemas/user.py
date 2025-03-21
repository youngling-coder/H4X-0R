from pydantic import BaseModel


class User(BaseModel):
    telegram_id: int
    reputation: float = 0.0
