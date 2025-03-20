from sqlalchemy import Column, Table, ForeignKey, BigInteger
from .base import Base


user_chat_association = Table(
    "user_chat",
    Base.metadata,
    Column(
        "user_id",
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE", name="fk_user_chat_user_id"),
        primary_key=True,
    ),
    Column(
        "chat_id",
        BigInteger,
        ForeignKey("chats.id", ondelete="CASCADE", name="fk_user_chat_chat_id"),
        primary_key=True,
    ),
)
