# from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy import create_engine
from decouple import config
from contextlib import contextmanager


DATABASE_URL = config("DATABASE_URL", default="sqlite: ///repos.db")
engine = create_engine(DATABASE_URL)
# engine = create_async_engine(DATABASE_URL, echo=True)

SessionLocal: sessionmaker = sessionmaker(bind=engine, expire_on_commit=False, autoflush=False, autocommit=False)
Base = declarative_base()

@contextmanager
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    except Exception as e:
        print(e)
        db.rollback()
    finally:
        db.close()