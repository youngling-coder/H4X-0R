from pydantic import BaseModel


class Message(BaseModel):
    id: int
    chat_id: int
    user_id: int
    content: str
    generation_time_ms: int
    history_part: bool
    from_bot: bool
