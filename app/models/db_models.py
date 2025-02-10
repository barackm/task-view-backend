from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class DBTask(BaseModel):
    id: Optional[str] = None
    title: str
    description: str
    priority: str
    estimated_duration: str
    duration_explanation: str
    assignee_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class DBUser(BaseModel):
    id: str
    full_name: str
    skills: List[str]
    email: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
