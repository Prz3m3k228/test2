from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.reservation import Reservation
from models.user import User
from models.car import Car
from schemas.reservations_schema import ReservationCreate, ReservationUpdate
from datetime import timedelta, datetime
from fastapi import HTTPException, status


def get_or_404(db: Session, model, id: int, detail: str):
    instance = db.query(model).filter(model.id == id).first()
    if not instance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
    return instance

def create_reservation(db: Session, reservation: ReservationCreate):
    user = get_or_404(db, User, reservation.user_id, "User not found")
    car = get_or_404(db, Car, reservation.car_id, "Car not found")

    # Walidacja poprawności dat
    if reservation.start_date < datetime.now():
        raise HTTPException(
            status_code=400,
            detail="Start date cannot be in the past."
        )
    if reservation.start_date >= reservation.end_date:
        raise HTTPException(
            status_code=400,
            detail="Start date must be earlier than end date."
        )

    # Sprawdzenie kolizji dat
    overlapping_reservations = db.query(Reservation).filter(
        Reservation.car_id == reservation.car_id,
        and_(
            Reservation.start_date <= reservation.end_date,
            Reservation.end_date >= reservation.start_date
        )
    ).all()

    if overlapping_reservations:
        raise HTTPException(
            status_code=400,
            detail="The car is already reserved for the selected dates."
        )

    # Tworzenie rezerwacji
    db_reservation = Reservation(**reservation.dict())
    db.add(db_reservation)

    # Aktualizacja statusu samochodu
    car.availability = "rented"
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

def get_reservation(db: Session, reservation_id: int):
    return get_or_404(db, Reservation, reservation_id, "Reservation not found")

def get_reservations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Reservation).offset(skip).limit(limit).all()

def update_reservation(db: Session, reservation_id: int, reservation: ReservationUpdate):
    db_reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if db_reservation:
        for key, value in reservation.dict(exclude_unset=True).items():
            setattr(db_reservation, key, value)
        db.commit()
        db.refresh(db_reservation)
    return db_reservation

def delete_reservation(db: Session, reservation_id: int):
    db_reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if db_reservation:
        db.delete(db_reservation)
        db.commit()
    return db_reservation

def cancel_reservation(db: Session, reservation_id: int):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if reservation:
        car = get_or_404(db, Car, reservation.car_id, "Car not found")
        db.delete(reservation)
        db.commit()

        # Sprawdzenie, czy samochód ma inne aktywne rezerwacje
        active_reservations = db.query(Reservation).filter(
            Reservation.car_id == car.id,
            Reservation.end_date >= datetime.now()
        ).count()

        if active_reservations == 0:
            car.availability = "available"
            db.commit()

        return True
    return False

def get_available_dates(db: Session, car_id: int):
    reservations = db.query(Reservation).filter(Reservation.car_id == car_id).all()
    occupied_dates = set()
    for reservation in reservations:
        current_date = reservation.start_date
        while current_date <= reservation.end_date:
            occupied_dates.add(current_date.date())
            current_date += timedelta(days=1)
    today = datetime.now().date()
    available_dates = [
        (today + timedelta(days=i)).isoformat()
        for i in range(30)
        if (today + timedelta(days=i)) not in occupied_dates
    ]
    return available_dates

def get_occupied_dates(db: Session, car_id: int):
    reservations = db.query(Reservation).filter(Reservation.car_id == car_id).all()
    occupied_dates = []
    for reservation in reservations:
        current_date = reservation.start_date
        while current_date <= reservation.end_date:
            occupied_dates.append(current_date.date().isoformat())
            current_date += timedelta(days=1)
    return occupied_dates
