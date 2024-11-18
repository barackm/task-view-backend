from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    """
    Shared properties across all User schemas.
    """
    first_name: Optional[str]
    last_name: Optional[str]
    email: EmailStr


class UserCreate(UserBase):
    """
    Schema for creating a new user.
    """
    first_name: str
    last_name: str
    email: EmailStr
    password: str 


class UserResponse(UserBase):
    """
    Schema for returning user details (excluding sensitive data).
    """
    id: int

    class Config:
        from_attributes = True



class UserLogin(BaseModel):
    """
    Schema for user login.
    """
    email: EmailStr
    password: str