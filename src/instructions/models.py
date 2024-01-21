from sqlalchemy import Column, Integer, String

from src.database.database import Base


class Instruction(Base):
    __tablename__ = "instructions"

    id: int = Column(Integer, primary_key=True)
    title: str = Column(String(length=150), nullable=False)
    description: str = Column(String(length=200), nullable=False)
