from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.db.models import User
from .schema import UserCreate
from app.utilities.security import hash_password

def create_user(db: Session, user_data: UserCreate):
    """
    Create a new user in the database.
    """
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = hash_password(user_data.password)
    
    new_user = User(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        password=hashed_password,
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

def get_user_by_email(db: Session, email: str):
    """
    Retrieve a user by email.
    """
    user = db.query(User).filter(User.email == email).first()
    return user