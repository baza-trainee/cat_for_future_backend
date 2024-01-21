from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, func

from src.database.database import Base


class Hero(Base):
    __tablename__ = "hero"

    id: int = Column(Integer, primary_key=True)
    title: str = Column(String(length=200), nullable=True)
    sub_title: str = Column(String(length=200), nullable=True)
    media_path: str = Column(String(length=500), nullable=False)
    left_text: str = Column(String(length=200), nullable=True)
    righth_text: str = Column(String(length=200), nullable=True)
    created_at: datetime = Column(DateTime, default=func.now())
