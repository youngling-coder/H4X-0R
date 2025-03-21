from typing import Optional

from pydantic import BaseModel


class Message(BaseModel):
    telegram_id: Optional[int] = None
    chat_id: int
    user_id: int
    content: str
    generation_time_ms: int = 0
    history_part: bool
    from_bot: bool
