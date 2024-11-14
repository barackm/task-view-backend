from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum
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
    
class TaskStatusEnum(str, Enum):
    PENDING = "Pending"
    IN_PROGRESS = "InProgress"
    COMPLETED = "Completed"

class TaskPriorityEnum(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class TaskSearchSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    statuses: Optional[List[str]] = None
    priorities: Optional[List[str]] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    assignee_ids: Optional[List[int]] = None