from database import Base
from sqlalchemy import Column, String, Text
import uuid


class LLMModel(Base):
    __tablename__ = "llm_models"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    model_id = Column(String, unique=True, index=True)
    provider = Column(String)
    api_key = Column(String, nullable=True)


class Repository(Base):
    __tablename__ = "repositories"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    url = Column(String, unique=True)


class CommitData(Base):
    __tablename__ = "commit_data"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    repo_id = Column(String, index=True)
    commit_message = Column(Text)
    git_diff = Column(Text)


class WorkSheet(Base):
    __tablename__ = "worksheets"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, index=True)
    sheet_id = Column(String, unique=True)
