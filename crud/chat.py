from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_session_required
import models, schemas
from typing import Optional


@db_session_required
async def add_user_to_chat_if_not_added(user_id: int, chat_id: int, db: AsyncSession):

    stmt = select(models.user_chat_association).where(
        models.user_chat_association.c.user_id == user_id,
        models.user_chat_association.c.chat_id == chat_id,
    )
    exists = (await db.execute(stmt)).first()

    if not exists:
        stmt = insert(models.user_chat_association).values(
            user_id=user_id, chat_id=chat_id
        )
        await db.execute(stmt)
        await db.commit()

    await db.close()


@db_session_required
async def get_chat_user_ids(telegram_id: int, db: AsyncSession):

    chat: models.Chat = await get_chat(telegram_id)
    
    stmt = select(models.user_chat_association.c.user_id).filter(models.user_chat_association.c.chat_id == chat.id)
    result = await db.execute(stmt)
    users = result.scalars().all()

    await db.close()

    return users


@db_session_required
async def get_chat(telegram_id: int, db: AsyncSession) -> Optional[models.Chat]:

    stmt = select(models.Chat).filter(models.Chat.telegram_id == telegram_id)
    result = await db.execute(stmt)
    chat = result.scalars().first()

    await db.close()

    return chat


@db_session_required
async def create_chat(chat: schemas.Chat, db: AsyncSession):

    chat_exists = await get_chat(chat.telegram_id)

    if not chat_exists:
        chat = models.Chat(**chat.model_dump())

        db.add(chat)
        await db.commit()
        await db.refresh(chat)
        await db.close()

        return chat
