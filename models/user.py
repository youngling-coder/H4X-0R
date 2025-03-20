from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Float
from typing import List, TYPE_CHECKING
from .user_chat import user_chat_association


if TYPE_CHECKING:
    from .chat import Chat
    from .message import Message


class User(Base):

    reputation: Mapped[float] = mapped_column(Float, default=0.0)

    chats: Mapped[List["Chat"]] = relationship(
        secondary=user_chat_association, back_populates="users"
    )
    messages: Mapped[List["Message"]] = relationship(back_populates="user")
