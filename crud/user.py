from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import db_session_required
import models, schemas


@db_session_required
async def get_user(user_id: int, db: AsyncSession):

    stmt = select(models.User).filter(models.User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalars().first()

    await db.close()

    return user


@db_session_required
async def create_user_if_not_exists(user: schemas.User, db: AsyncSession):

    user_exists = await get_user(user.id)

    if not user_exists:

        user = models.User(id=user.id)

        db.add(user)
        await db.commit()
        await db.refresh(user)
        await db.close()

        return user
