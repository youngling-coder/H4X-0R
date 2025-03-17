from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from settings import h4x0r_settings

DATABASE_URL = f"sqlite:///{h4x0r_settings.DATABASE_FILE}"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}, echo=False
)

SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)


# Dependency for getting DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
