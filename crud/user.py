from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_session_required
import models, schemas


@db_session_required
async def get_user_by_telegram_id(telegram_id: int, db: AsyncSession):

    stmt = select(models.User).filter(models.User.telegram_id == telegram_id)
    result = await db.execute(stmt)
    user = result.scalars().first()

    await db.close()

    return user


@db_session_required
async def get_user_by_id(user_id: int, db: AsyncSession):

    stmt = select(models.User).filter(models.User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalars().first()

    await db.close()

    return user


@db_session_required
async def create_user(user_schema: schemas.User, db: AsyncSession):

    user = models.User(**user_schema.model_dump())

    db.add(user)
    await db.commit()
    await db.refresh(user)
    await db.close()

    return user


@db_session_required
async def create_user_if_not_exists_update_otherwise(
    user_schema: schemas.User, db: AsyncSession
):

    user = await get_user_by_telegram_id(user_schema.telegram_id)

    if not user:
        await create_user(user_schema)

    else:
        stmt = (
            update(models.User)
            .where(models.User.telegram_id == user_schema.telegram_id)
            .values(**user_schema.model_dump())
            .returning(models.User)
        )
        result = await db.execute(stmt)
        user = result.scalars().first()
        await db.commit()

    await db.close()

    return user
