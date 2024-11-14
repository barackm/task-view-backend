from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    tags: Optional[List[str]] = None

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    tags: Optional[str] = None

    class Config:
        from_attributes = True


class TagRequest(BaseModel):
    tag: str
    action: str 