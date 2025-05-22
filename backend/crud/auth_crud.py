from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models import User
from schemas.auth_schema import UserLogin
from utils.hash import verify_password
from utils.jwt import create_access_token

# Funkcja do logowania użytkownika
def login_user(db: Session, user: UserLogin):
    user_in_db = db.query(User).filter(User.email == user.email).first()

    if not user_in_db or not verify_password(user.password, user_in_db.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Generowanie tokenu JWT z danymi użytkownika
    user_data = {"sub": user_in_db.email, "role": user_in_db.role}
    access_token = create_access_token(data=user_data)

    return {"access_token": access_token, "token_type": "bearer"}