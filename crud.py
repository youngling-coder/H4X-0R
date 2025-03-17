from sqlalchemy.orm import Session
from models import Chat, Message
from database import get_db
from typing import Literal


def create_chat(chat_id: str, db: Session = next(get_db())):
    chat = Chat(id=chat_id)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat


def get_chat(chat_id: str, db: Session = next(get_db())):
    return db.query(Chat).filter(Chat.id == chat_id).first()


def create_message(
    chat_id: str,
    content: str,
    role: Literal["user", "model"],
    db: Session = next(get_db()),
):
    message = Message(chat_id=chat_id, role=role, content=content)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def get_messages(chat_id: str, db: Session = next(get_db())):
    return db.query(Message).filter(Message.chat_id == chat_id).all()


def delete_chat(chat_id: str, db: Session = next(get_db())):
    chat = get_chat(db, chat_id)
    if chat:
        db.delete(chat)
        db.commit()
        return True
    return False


def get_chat_history(chat_id: str):
    history = []

    for message in get_messages(chat_id=chat_id):

        history.append(
            {
                "role": message.role.value,
                "parts": [message.content],
            }
        )

    return history
