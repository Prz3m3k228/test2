from fastapi import APIRouter, HTTPException, status, Depends, Header, Query
from fastapi.security import OAuth2PasswordBearer
from typing import List
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from api.dependencies import get_db
from crud.user_crud import create_user,update_user,delete_user,get_users,greet_user,admin_update_user
from schemas.user_schema import UserCreate, UserUpdate, UserResponse, AdminUserUpdate
from utils.jwt import get_current_user
from models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter()

################### Endpointy dla wszystkich użytkowników ###################

# Endpoint do tworzenia nowego użytkownika
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = create_user(db=db, user_data=user)
        return new_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

################### Endpointy dla użytkowników zalgowanych (logged-in users) ###################

# Endpoint do aktualizacji istniejącego użytkownika na podstawie jego ID (dla zwykłego użytkownika)
@router.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_current_user(
    user_id: int, 
    user: UserUpdate,
    db: Session = Depends(get_db),
    token: str = Query(..., description="JWT token to authenticate user")
):
    # Weryfikacja tokenu i uzyskanie danych użytkownika
    current_user_data = get_current_user(token)
    current_role = current_user_data.get("role")
    current_user_email = current_user_data.get("email")

    # Sprawdzamy, czy użytkownik próbuje zaktualizować swoje dane
    if current_role != "admin" and current_user_email != db.query(User).filter(User.id == user_id).first().email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update this user's data"
        )

    updated_user = update_user(db=db, user_id=user_id, user_data=user)
    return updated_user

# Endpoint do usunięcia użytkownika na podstawie jego ID (dla zwykłego użytkownika)
@router.delete("/{user_id}", status_code=status.HTTP_200_OK)
def delete_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    token: str = Query(..., description="JWT token to authenticate user")
):
    # Weryfikacja poprawności tokena
    get_current_user(token)

    try:
        delete_user(db=db, user_id=user_id)
        return JSONResponse(content={"message": "Successfully deleted user"}, status_code=200)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# Endpoint do powitania użytkownika po ID
@router.get("/{user_id}/greet")
def greet_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    token: str = Query(..., description="JWT token to authenticate user")
):
    # Weryfikacja poprawności tokena
    get_current_user(token)

    try:
        message = greet_user(db=db, user_id=user_id)
        return {"message": message}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
################### Endpointy dla administratorów ###################

# Endpoint wyświetlający wszystkich użytkowników na bazie danych (tylko dla adminów)
@router.get("/admin", response_model=List[UserResponse])
def read_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    token: str = Query(..., description="JWT token to authenticate user"),
    db: Session = Depends(get_db)
):
    current_user_data = get_current_user(token)
    current_role = current_user_data.get("role")

    if current_role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can access the list of users."
        )

    users = get_users(db=db, skip=skip, limit=limit)
    return users

# Endpoint do aktualizacji istniejącego użytkownika na podstawie jego ID (tylko dla adminów)
@router.put("/admin/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user_by_admin(
    user_id: int,
    user_data: AdminUserUpdate,
    db: Session = Depends(get_db),
    token: str = Query(..., description="JWT token with admin privileges")
):

    current_user_data = get_current_user(token)
    current_role = current_user_data.get("role")
    
    if current_role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can access the list of users."
        )
    try:
        updated_user = admin_update_user(db=db, user_id=user_id, user_data=user_data)
        return updated_user
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))