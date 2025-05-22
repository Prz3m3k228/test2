from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal
from datetime import datetime

# Schemat do tworzenia nowego użytkownika
class UserCreate(BaseModel):
    name: str = Field(..., example="John")
    surname: Optional[str] = Field(None, example="Doe")
    email: EmailStr = Field(..., example="john.doe@example.com")
    address: str = Field(..., example="123 Main Street")
    city: str = Field(..., example="New York")
    password: str = Field(..., example="SecurePass123!")

    class Config:
        orm_mode = True

# Schemat do aktualizacji istniejącego użytkownika
class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Johnny")
    surname: Optional[str] = Field(None, example="Smith")
    email: Optional[EmailStr] = Field(None, example="johnny.smith@example.com")
    address: Optional[str] = Field(None, example="456 Oak Avenue")
    city: Optional[str] = Field(None, example="Los Angeles")
    password: Optional[str] = Field(None, example="NewSecurePass456!")

    class Config:
        orm_mode = True
        
# Schemat do aktualizacji istniejącego użytkownika dla administratora
class AdminUserUpdate(UserUpdate):
    role: Optional[Literal['user', 'admin']]

# Schemat do odpowiedzi użytkownika
class UserResponse(BaseModel):
    id: int = Field(..., example=1)
    name: str = Field(..., example="John")
    surname: Optional[str] = Field(None, example="Doe")
    email: EmailStr = Field(..., example="john.doe@example.com")
    address: str = Field(..., example="123 Main Street")
    city: str = Field(..., example="New York")
    role: str = Field(..., example="user")  # ← DODANE pole
    created_at: datetime = Field(..., example="2025-05-13T15:30:00")

    class Config:
        orm_mode = True