from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from src.database.database import Base


class Cat(Base):
    __tablename__ = "cats"

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(length=100), nullable=True)
    is_male: bool = Column(Boolean, server_default="true", nullable=False)
    is_reserved: bool = Column(Boolean, server_default="false", nullable=False)
    description: str = Column(String(2000), nullable=True)
    date_of_birth: Date = Column(Date, nullable=True)

    photos = relationship(
        "CatPhotos", back_populates="cat", cascade="all, delete-orphan"
    )

    user_id: int = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="cats", passive_deletes=True)


class CatPhotos(Base):
    __tablename__ = "cat_photos"

    id: int = Column(Integer, primary_key=True)
    cat_id = Column(Integer, ForeignKey("cats.id"))
    cat = relationship("Cat", back_populates="photos")
    media_path: str = Column(String(length=200), nullable=False)
