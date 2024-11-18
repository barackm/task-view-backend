from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import User
from app.utilities.token import decode_access_token


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, exempt_routes=None):
        super().__init__(app)
        self.exempt_routes = exempt_routes or []

    async def dispatch(self, request: Request, call_next):
        for route in self.exempt_routes:
            if request.url.path.startswith(route):
                return await call_next(request)

        authorization: str = request.headers.get("Authorization")
        if not authorization:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header missing",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token format",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token = authorization.split(" ")[1]

        try:
            payload = decode_access_token(token)
            user_id = payload.get("user_id")

            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token payload",
                )

            db: Session = next(get_db())
            user = db.query(User).filter(User.id == user_id).first()

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )

            request.state.user = user

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"},
            )

        response = await call_next(request)
        return response