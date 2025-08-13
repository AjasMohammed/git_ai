# from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from sqlalchemy import create_engine
from config import database_url

engine = create_engine(database_url)
# engine = create_async_engine(DATABASE_URL, echo=True)

SessionLocal: sessionmaker = sessionmaker(bind=engine, expire_on_commit=False, autoflush=False, autocommit=False)
Base = declarative_base()


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    except Exception as e:
        print(e)
        db.rollback()
    finally:
        db.close()