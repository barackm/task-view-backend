from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import User
from app.utilities.token import decode_access_token
import logging

logger = logging.getLogger(__name__)

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/auth/login") or request.url.path.startswith("/auth/register"):
            return await call_next(request)
        
        auth_header = request.scope["headers"]
        auth_header = dict(auth_header).get(b"authorization")
        if auth_header:
            auth_header = auth_header.decode("utf-8")
        
        if not auth_header:
            return JSONResponse(
                status_code=401,
                content={"detail": "Missing Authorization header"},
            )

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            logger.info("Invalid Authorization header format.")
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid Authorization header format. Expected 'Bearer <token>'"}
            )

        token = parts[1]
        try:
            payload = decode_access_token(token)
            print(payload)
        except Exception as e:
            logger.info(f"Token decoding failed: {e}")
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid or expired token"}
            )

        user_id = payload.get("sub")
        if not user_id:
            logger.info("Token payload missing 'sub' field.")
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid token payload"}
            )

        db: Session = next(get_db())
        try:
            user = db.query(User).filter(User.id == int(user_id)).first()
            if not user:
                logger.info("User not found for the given token.")
                return JSONResponse(
                    status_code=401,
                    content={"detail": "User not found or inactive"}
                )
        finally:
            db.close()

        request.state.user = user

        response = await call_next(request)
        return response