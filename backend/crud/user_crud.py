from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.user import User
from schemas.user_schema import UserCreate, UserUpdate, AdminUserUpdate
from datetime import datetime
from utils.hash import hash_password

# Funkcja tworząca nowego użytkownika
def create_user(db: Session, user_data: UserCreate) -> User:
    try:
        new_user = User(
            name=user_data.name,
            surname=user_data.surname,
            email=user_data.email,
            address=user_data.address,
            city=user_data.city,
            hashed_password=hash_password(user_data.password),
            created_at=datetime.utcnow(),
            role="admin"
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        db.rollback()
        raise ValueError("This email is already registered.")

# Funkcja aktualizująca istniejącego użytkownika
def update_user(db: Session, user_id: int, user_data: UserUpdate) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found.")

    if user_data.name:
        user.name = user_data.name
    if user_data.surname:
        user.surname = user_data.surname
    if user_data.email:
        user.email = user_data.email
    if user_data.address:
        user.address = user_data.address
    if user_data.city:
        user.city = user_data.city
    if user_data.password:
        user.hashed_password = hash_password(user_data.password)

    db.commit()
    db.refresh(user)
    return user

# Funkcja usuwająca użytkownika na podstawie jego ID
def delete_user(db: Session, user_id: int) -> bool:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found.")
    
    db.delete(user)
    db.commit()
    return True

# Funkcja pobierająca użytkownika na podstawie jego ID
def get_user(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found.")
    return user

# Funkcja powitania użytkownika na podstawie jego ID
def greet_user(db: Session, user_id: int) -> str:
    # Wyowłanie funkcji pomocniczej
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found.")
    return f"Witaj, {user.name}!"

# Funkcja aktualizująca istniejącego użytkownika dla administratora
def admin_update_user(db: Session, user_id: int, user_data: AdminUserUpdate) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found.")

    if user_data.name:
        user.name = user_data.name
    if user_data.surname:
        user.surname = user_data.surname
    if user_data.email:
        user.email = user_data.email
    if user_data.address:
        user.address = user_data.address
    if user_data.city:
        user.city = user_data.city
    if user_data.password:
        user.hashed_password = hash_password(user_data.password)
    
    if user_data.role:
        user.role = user_data.role  # Typ `Literal` już waliduje poprawność

    db.commit()
    db.refresh(user)
    return user

# Funkcja pobierająca wszystkich użytkowników dla administratora
def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    users = db.query(User).offset(skip).limit(limit).all()
    return users