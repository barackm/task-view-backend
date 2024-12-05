from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.db.models import User
from app.utilities.security import verify_password
from app.utilities.token import create_access_token

def authenticate_user(db: Session, email: str, password: str):
    """
    Authenticate a user by email and password.
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    return user

def login_user(db: Session, email: str, password: str):
    """
    Handle user login and return a JWT token.
    """
    user = authenticate_user(db, email, password)
    
    token = create_access_token(data={"user_id": user.id, "email": user.email})
    return {"access_token": token, "token_type": "bearer", "user": {"id": user.id, "email": user.email}}
