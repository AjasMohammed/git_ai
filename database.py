# from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine

DATABASE_URL = "sqlite:////db/repos.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# engine = create_async_engine(DATABASE_URL, echo=True)

SessionLocal: sessionmaker = sessionmaker(bind=engine, expire_on_commit=False, autoflush=False, autocommit=False)
Base = declarative_base()