from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_session_required
import models, schemas


@db_session_required
async def create_message(message: schemas.Message, db: AsyncSession):

    message = models.Message(**message.model_dump())

    db.add(message)
    await db.commit()
    await db.refresh(message)
    await db.close()

    return message


@db_session_required
async def get_messages(
    db: AsyncSession,
    chat_id: Optional[int] = None,
    user_id: Optional[int] = None,
    history_part: bool = False,
) -> list[models.Message]:

    stmt = select(models.Message)

    if isinstance(chat_id, int):
        stmt = stmt.filter(models.Message.chat_id == chat_id)

    if isinstance(user_id, int):
        stmt = stmt.filter(models.Message.user_id == user_id)

    if history_part:
        stmt = stmt.filter(models.Message.history_part == history_part)

    result = await db.execute(stmt)
    messages = result.scalars().all()

    await db.close()

    return messages


async def get_chat_history(chat_id: str) -> list[dict]:
    history = []

    messages: list[models.Message] = await get_messages(
        chat_id=chat_id, history_part=True
    )

    for message in messages:

        history.append(
            {
                "role": "model" if not message.from_bot else "user",
                "parts": [message.content],
            }
        )

    return history
