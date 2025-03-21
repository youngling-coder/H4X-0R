from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import text, Float, ForeignKey, Boolean, String, Integer, BigInteger
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .chat import Chat
    from .user import User


class Message(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    chat_id: Mapped[int] = mapped_column(
        ForeignKey("chats.id", ondelete="CASCADE", name="fk_message_chat_id")
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="NO ACTION", name="fk_message_user_id")
    )
    generation_time_ms: Mapped[float] = mapped_column(
        Float, nullable=False, server_default="0.0"
    )
    history_part: Mapped[bool] = mapped_column(Boolean, server_default=text("false"))
    from_bot: Mapped[bool] = mapped_column(
        Boolean, nullable=False, server_default=text("false")
    )
    content: Mapped[str] = mapped_column(String, nullable=False)

    chat: Mapped["Chat"] = relationship(back_populates="messages")
    user: Mapped["User"] = relationship(back_populates="messages")

