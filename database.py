from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from settings import h4x0r_settings
from functools import wraps

DATABASE_URL = f"postgresql+asyncpg://{h4x0r_settings.DB_USER}:{h4x0r_settings.DB_PASS}@{h4x0r_settings.DB_HOST}:{h4x0r_settings.DB_PORT}/{h4x0r_settings.DB_NAME}"

engine = create_async_engine(DATABASE_URL, echo=False)

async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db():
    async with async_session() as session:
        return session


def db_session_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # Ensure `db` is in kwargs, otherwise call `get_session`
        if "db" not in kwargs:
            kwargs["db"] = await get_db()

        # Now call the actual function with the session
        return await func(*args, **kwargs)

    return wrapper
