from pydantic import BaseModel, Field
from typing import List, Optional

# Schemat bazowy samochodu – używany jako podstawa do tworzenia i odczytu danych
class CarBase(BaseModel):
    brand: str = Field(..., example="Toyota")
    model: str = Field(..., example="Corolla")
    year: int = Field(..., example=2022)
    color: str = Field(..., example="Red")
    price_per_day: float = Field(..., example=100)
    availability: Optional[str] = Field(default="available", example="available")  # np. "available", "rented"

# Schemat do tworzenia nowego samochodu
class CarCreate(CarBase):
    pass

# Schemat do aktualizacji danych samochodu (wszystkie pola opcjonalne)
class CarUpdate(BaseModel):
    brand: Optional[str] = Field(None, example="Toyota")
    model: Optional[str] = Field(None, example="Corolla")
    year: Optional[int] = Field(None, example=2022)
    color: Optional[str] = Field(None, example="Red")
    price_per_day: Optional[float] = Field(None, example=100)
    availability: Optional[str] = Field(None, example="available")

# Schemat zwracany w odpowiedziach API – zawiera pełne dane samochodu wraz z ID
class Car(CarBase):
    id: int

    class Config:
        orm_mode = True

# Schemat listy samochodów – np. jako wynik zapytania o wszystkie dostępne samochody
class CarListSchema(BaseModel):
    cars: List[Car]
