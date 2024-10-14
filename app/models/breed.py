from sqlalchemy import Column, Integer, String
from app.database import Base
from sqlalchemy.orm import relationship


class Breed(Base):
    __tablename__ = 'breeds'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    weight = Column(String, nullable=True)
    height = Column(String, nullable=True)
    life_span = Column(String, nullable=True)
    bred_for = Column(String, nullable=True)
    breed_group = Column(String, nullable=True)
    images = relationship("Image", back_populates="breed", cascade="all, delete-orphan")