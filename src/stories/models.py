from sqlalchemy import Column, Integer, String

from src.database.database import Base


class Story(Base):
    __tablename__ = "stories"

    id: int = Column(Integer, primary_key=True)
    title: str = Column(String(length=120), nullable=True)
    text: str = Column(String(2000), nullable=True)
    media_path: str = Column(String(length=500), nullable=False)
