from sqlalchemy import Column, Integer, String

from src.database.database import Base


class Accountability(Base):
    __tablename__ = "accountability"

    id: int = Column(Integer, primary_key=True)
    media_path: str = Column(String(length=500), nullable=False)
