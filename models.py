from database import Base
from sqlalchemy import Column, String
import uuid

class Repository(Base):
    __tablename__ = "repositories"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, index=True)
    url = Column(String, unique=True, index=True)
