from sqlalchemy.orm import Session
from sqlalchemy import func
import models
from database import get_db
from typing import Literal


def create_chat(chat_id: str, db: Session = next(get_db())):

    if not (get_chat(chat_id)):
        chat = models.Chat(id=chat_id)
        db.add(chat)
        db.commit()
        db.refresh(chat)
        return chat


def get_chat(chat_id: str, db: Session = next(get_db())):
    return db.query(models.Chat).filter(models.Chat.id == chat_id).first()


def create_message(
    chat_id: str,
    content: str,
    role: Literal["user", "model"],
    db: Session = next(get_db()),
):
    message = models.Message(chat_id=chat_id, role=role, content=content)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def get_messages(chat_id: str, db: Session = next(get_db())):
    return db.query(models.Message).filter(models.Message.chat_id == chat_id)


def get_amount_messages_in_chat(chat_id: str, db: Session = next(get_db())):
    return db.query(
        func.count(models.Message.id).filter(models.Message.chat_id == chat_id)
    ).scalar()


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


def get_user(user_id: str, db: Session = next(get_db())):
    return db.query(
        func.count(models.User.id).filter(models.User.id == user_id)
    ).scalar()


def create_user_if_not_exists(user_id: str, db: Session = next(get_db())):

    if not get_user(user_id):

        user = models.User(id=user_id)

        db.add(user)
        db.commit()
        db.refresh(user)

        return user
