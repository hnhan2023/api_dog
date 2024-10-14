from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime


class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True, index=True)
    image_path = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)  
    breed_id = Column(Integer, ForeignKey("breeds.id"))
    breed = relationship("Breed", back_populates="images")