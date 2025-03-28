from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, Float, Integer, String
from typing import List, TYPE_CHECKING, Optional
from .user_chat import user_chat_association


if TYPE_CHECKING:
    from .chat import Chat
    from .message import Message


class User(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    username: Mapped[Optional[str]] = mapped_column(String, unique=True, nullable=True)
    reputation: Mapped[float] = mapped_column(Float, default=0.0)

    chats: Mapped[List["Chat"]] = relationship(
        secondary=user_chat_association, back_populates="users"
    )
    messages: Mapped[List["Message"]] = relationship(back_populates="user")
