from sqlalchemy import Column, Integer,ForeignKey, String, DateTime, func
from sqlalchemy.orm import relationship
from database import Base

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    car_id = Column(Integer, ForeignKey("cars.id"), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    status = Column(String, default="active")

    # Relacje
    user = relationship("User", back_populates="reservations")
    car = relationship("Car", back_populates="reservations")