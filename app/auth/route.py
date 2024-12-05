from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.modules.users.service import create_user, get_user_by_email
from app.modules.users.schema import UserCreate, UserLogin
from app.utilities.token import create_access_token
from app.db.models import User
from app.utilities.security import verify_password
from app.auth.dependencies import get_current_user

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.
    """
    user = create_user(db, user_data)
    access_token = create_access_token(data={"user_id": user.id, "email": user.email})
    return {"access_token": access_token, "token_type": "Bearer"}


@router.post("/login")
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user and return a JWT token.
    """
    print(user_credentials, "user_credentials")
    user = db.query(User).filter(User.email == user_credentials.email).first()
    print(user, "user")
    if not user or not verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": str(user.id), "email": user.email})
    return {"access_token": access_token, "token_type": "Bearer"}

@router.get("/me")
async def me(request: Request):
    """
    Get the current user's data.
    """
    
    token  =  request.headers.get("Authorization")
    print(token, "token")
    user = getattr(request.state, "user", None)
    if user:
        print(user, "request.state")
        return {"first_name": user.first_name, "email": user.email, "id": user.id, "last_name": user.last_name}
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")