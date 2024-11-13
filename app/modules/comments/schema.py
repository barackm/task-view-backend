from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CommentCreate(BaseModel):
    task_id: int
    content: str

class CommentUpdate(BaseModel):
    content: Optional[str] = None

class CommentResponse(BaseModel):
    id: int
    task_id: int
    user_id: int
    content: str
    created_at: datetime

    class Config:
        from_attributes = True
