from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_session_required
import models, schemas


@db_session_required
async def get_user(telegram_id: int, db: AsyncSession):

    stmt = select(models.User).filter(models.User.telegram_id == telegram_id)
    result = await db.execute(stmt)
    user = result.scalars().first()

    await db.close()

    return user


@db_session_required
async def create_user_if_not_exists(user_schema: schemas.User, db: AsyncSession):

    user = await get_user(user_schema.telegram_id)

    if not user:

        user = models.User(**user_schema.model_dump())

        db.add(user)
        await db.commit()
        await db.refresh(user)
        await db.close()

    return user
