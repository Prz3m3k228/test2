from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.car_schema import Car, CarCreate, CarUpdate
from crud.cars_crud import get_all_cars, get_car_by_id, create_car, update_car, delete_car
from api.dependencies import get_db

router = APIRouter()

################### Endpointy dla wszystkich użytkowników ###################

# Endpoint do pobierania wszystkich samochodów
@router.get("/", response_model=list[Car])
def read_all_cars(db: Session = Depends(get_db)):
    return get_all_cars(db)

# Endpoint do pobierania konkretnego samochodu po ID
@router.get("/{car_id}", response_model=Car)
def read_car(car_id: int, db: Session = Depends(get_db)):
    car = get_car_by_id(db, car_id)
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")
    return car

################### Endpointy dla administratorów ###################

# Endpoint do tworzenia nowego samochodu (tylko dla adminów)
@router.post("/admin", status_code=status.HTTP_201_CREATED)
def create_new_car(car: CarCreate, db: Session = Depends(get_db)):
    create_car(db, car)
    return {"message": "Car created successfully"}

# Endpoint do edycji istniejącego samochodu (tylko dla adminów)
@router.put("/admin/{car_id}", response_model=Car)
def update_existing_car(car_id: int, car: CarUpdate, db: Session = Depends(get_db)):
    updated_car = update_car(db, car_id, car)
    if not updated_car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")
    return updated_car

# Endpoint do usuwania istniejącego samochodu (tylko dla adminów)
@router.delete("/admin/{car_id}")
def delete_existing_car(car_id: int, db: Session = Depends(get_db)):
    success = delete_car(db, car_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")
    return {"message": "Car deleted successfully"}
