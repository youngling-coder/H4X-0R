from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    telegram_id: int
    reputation: float = 0.0
    name: str
    username: Optional[str] = None