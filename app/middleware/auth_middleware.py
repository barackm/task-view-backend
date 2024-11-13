from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import User
from starlette.datastructures import State

SIMULATED_TOKEN = "mock-token"

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = request.headers.get("Authorization") or f"Bearer {SIMULATED_TOKEN}"
        if token == f"Bearer {SIMULATED_TOKEN}":
            db: Session = next(get_db())
            user = db.query(User).filter(User.id == 1).first()
            print(user)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

            request.state.user = user
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or missing authorization token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        response = await call_next(request)
        return response
