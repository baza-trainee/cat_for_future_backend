from sqlalchemy import Column, Integer, String

from src.database.database import Base


class Document(Base):
    __tablename__ = "documents"

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(length=100), nullable=False)
    media_path: str = Column(String(length=500), nullable=False)
