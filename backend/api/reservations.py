from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from datetime import datetime
from schemas.reservations_schema import Reservation, ReservationCreate
from crud.reservations_crud import create_reservation,cancel_reservation,get_available_dates,get_occupied_dates,delete_reservation
from api.dependencies import get_db

router = APIRouter()

def fix_date_format(dt_str):
    if dt_str and isinstance(dt_str, str):
        if dt_str.endswith("+02"):
            dt_str = dt_str + ":00"
        return datetime.fromisoformat(dt_str)
    return dt_str

################### Endpointy dla wszystkich użytkowników ###################

# Endpoint do pobierania dostępnych dat dla danego samochodu
@router.get("/available-dates", response_model=List[str])
def available_dates(car_id: int, db: Session = Depends(get_db)):
    return get_available_dates(db, car_id)

################### Endpointy dla użytkowników zalgowanych (logged-in users) ###################

# Endpoint do tworzenia nowej rezerwacji
@router.post("/", response_model=Reservation)
def make_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
    created_reservation = create_reservation(db, reservation)
    if created_reservation:
        created_reservation.start_date = fix_date_format(created_reservation.start_date)
        created_reservation.end_date = fix_date_format(created_reservation.end_date)
    else:
        raise HTTPException(status_code=400, detail="Reservation could not be created")
    return created_reservation

# Endpoint do anulowania rezerwacji
@router.delete("/{reservation_id}", response_model=dict)
def cancel_reservation_endpoint(reservation_id: int, db: Session = Depends(get_db)):
    success = cancel_reservation(db, reservation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return {"detail": "Reservation canceled successfully"}

################### Endpointy dla administratorów ###################

# Endpoint do pobierania zajętych dat dla danego samochodu
@router.get("/admin/occupied-dates", response_model=List[str])
def occupied_dates(car_id: int, db: Session = Depends(get_db)):
    return get_occupied_dates(db, car_id)

# Endpoint do usunięcia rezerwacji
@router.delete("/admin/{reservation_id}")
def delete_reservation_endpoint(reservation_id: int, db: Session = Depends(get_db)):
    reservation = delete_reservation(db, reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return {"detail": f"Reservation {reservation_id} has been deleted successfully."}

