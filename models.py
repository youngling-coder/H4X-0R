from sqlalchemy import String, Integer, ForeignKey, Enum
from sqlalchemy.orm import mapped_column, Mapped, relationship
import enum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserRole(enum.Enum):
    user = "user"
    model = "model"


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[str] = mapped_column(
        String, nullable=False, unique=True, primary_key=True
    )
    messages: Mapped[list["Message"]] = relationship(
        "Message", back_populates="chat", cascade="all, delete"
    )


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(
        Integer, nullable=False, unique=True, primary_key=True
    )
    chat_id: Mapped[str] = mapped_column(ForeignKey("chats.id", ondelete="CASCADE"))
    chat: Mapped["Chat"] = relationship("Chat", back_populates="messages")
    content: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String, nullable=False, unique=True, primary_key=True
    )
    reputation: Mapped[int] = mapped_column(Integer, nullable=False, server_default="0")