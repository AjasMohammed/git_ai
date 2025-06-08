from database import Base
from sqlalchemy import Column, String, Text
import uuid

class Repository(Base):
    __tablename__ = "repositories"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, index=True)
    url = Column(String, unique=True, index=True)


class CommitData(Base):
    __tablename__ = "commit_data"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    repo_id = Column(String, index=True)
    commit_message = Column(Text)
    git_diff = Column(Text)