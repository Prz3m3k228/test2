from sqlalchemy.orm import Session
from models.car import Car
from schemas.car_schema import CarCreate, CarUpdate
from fastapi import HTTPException, status
from datetime import datetime

# funkcja do pobierania wszystkich samochodów z bazy danych
def get_all_cars(db: Session):
    return db.query(Car).all()

# funkcja do pobierania samochodu po jego ID
def get_car_by_id(db: Session, car_id: int):
    return db.query(Car).filter(Car.id == car_id).first()

# funkcja do tworzenia nowego samochodu w bazie danych
def create_car(db: Session, car: CarCreate):
    # Walidacja roku produkcji
    current_year = datetime.now().year
    if car.year < 1886 or car.year > current_year:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid year: {car.year}. Year must be between 1886 and {current_year}."
        )
    
    # Walidacja ceny wynajmu
    if car.price_per_day <= 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Price per day must be greater than 0."
        )
    
    # Tworzenie samochodu
    db_car = Car(**car.dict())
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car

# funkcja do aktualizacji istniejącego samochodu o podanym ID
def update_car(db: Session, car_id: int, car: CarUpdate):
    db_car = get_car_by_id(db, car_id)
    if not db_car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Car with ID {car_id} not found."
        )

    # Walidacja roku produkcji (jeśli podano)
    if car.year is not None:
        current_year = datetime.now().year
        if car.year < 1886 or car.year > current_year:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Invalid year: {car.year}. Year must be between 1886 and {current_year}."
            )

    # Walidacja ceny wynajmu (jeśli podano)
    if car.price_per_day is not None and car.price_per_day <= 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Price per day must be greater than 0."
        )

    # Aktualizacja pól samochodu
    for key, value in car.dict(exclude_unset=True).items():
        setattr(db_car, key, value)
    db.commit()
    db.refresh(db_car)
    return db_car

# funkcja do usuwania samochodu o podanym ID z bazy danych
def delete_car(db: Session, car_id: int):
    db_car = get_car_by_id(db, car_id)
    if db_car:
        db.delete(db_car)
        db.commit()
        return True
    return False
