from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Float, BigInteger, Integer
from typing import List, TYPE_CHECKING

from .user_chat import user_chat_association

if TYPE_CHECKING:
    from .user import User
    from .message import Message


class Chat(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    api_key: Mapped[str] = mapped_column(String, nullable=True)
    tts_model: Mapped[str] = mapped_column(
        String, nullable=False, server_default="TeraTTS/glados2-g2p-vits"
    )
    history_depth: Mapped[int] = mapped_column(
        BigInteger, nullable=False, server_default="1000"
    )
    tts_length_scale: Mapped[float] = mapped_column(
        Float, nullable=False, server_default="1.2"
    )

    users: Mapped[List["User"]] = relationship(
        secondary=user_chat_association, back_populates="chats"
    )
    messages: Mapped[List["Message"]] = relationship(back_populates="chat")
