from fastapi import APIRouter, Request
from app.modules.users.schema import UserResponse
from app.db.models import User

router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def get_current_user(request: Request) -> UserResponse:
    """
    Retrieve the currently authenticated user's details.
    """
    user: User = request.state.user
    return UserResponse(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email
    )