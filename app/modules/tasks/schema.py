from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.db.models import TaskStatus, TaskPriority

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    project_id: int
    assigned_to: Optional[int] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: TaskStatus
    priority: TaskPriority
    created_at: datetime
    updated_at: datetime
    project_id: int
    assigned_to: Optional[int] = None

    class Config:
        from_attributes = True

class TaskAssign(BaseModel):
    user_id: int