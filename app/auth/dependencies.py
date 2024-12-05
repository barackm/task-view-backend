from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import User

def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    user = db.query(User).filter(User.id == request.state.user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
