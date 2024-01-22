from sqlalchemy import Column, Integer, String

from src.database.database import Base


class Contacts(Base):
    __tablename__ = "contacts"

    id: int = Column(Integer, primary_key=True)
    phone: str = Column(String(length=30), nullable=False)
    email: str = Column(String(length=100), nullable=False)
    post_address: str = Column(String(length=200))
    facebook: str = Column(String(length=500))
    instagram: str = Column(String(length=500))
