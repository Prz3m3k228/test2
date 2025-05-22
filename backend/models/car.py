from sqlalchemy import Column, Integer, String, func
from sqlalchemy.orm import relationship
from database import Base

class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    color = Column(String, nullable=False)
    price_per_day = Column(Integer, nullable=False)
    availability = Column(String, default="available", nullable=False)
    # pozniej dodac zdjecie

    # Relacje
    reservations = relationship("Reservation", back_populates="car")
    reviews = relationship("Review", back_populates="car")