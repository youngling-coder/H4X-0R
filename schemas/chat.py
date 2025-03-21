from pydantic import BaseModel


class Chat(BaseModel):
    telegram_id: int
    api_key: str = ""
    tts_model: str | None = None
    history_depth: int | None = None
    tts_length_scale: float | None = None
