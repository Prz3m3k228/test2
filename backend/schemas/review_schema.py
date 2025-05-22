from pydantic import BaseModel, Field
from typing import Optional

# Schemat bazowy recenzji – zawiera ocenę i opcjonalny komentarz
class ReviewBase(BaseModel):
    rating: int = Field(..., ge=1, le=5, example=4)  # Ocena w skali od 1 do 5
    comment: Optional[str] = Field(None, example="Very comfortable car!")

# Schemat do tworzenia nowej recenzji
class ReviewCreate(ReviewBase):
    user_id: int = Field(..., example=1)
    car_id: int = Field(..., example=2)

# Schemat do aktualizacji recenzji (wszystkie pola opcjonalne)
class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5, example=5)
    comment: Optional[str] = Field(None, example="Updated comment")

# Schemat zwracany w odpowiedziach API
class Review(ReviewBase):
    id: int
    user_id: int
    car_id: int

    class Config:
        orm_mode = True
