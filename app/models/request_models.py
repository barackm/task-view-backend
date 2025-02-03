from pydantic import BaseModel
from typing import List, Optional


class UserTask(BaseModel):
    title: str
    priority: str


class TaskData(BaseModel):
    title: str
    description: str
    priority: str = "Medium"


class UserProfile(BaseModel):
    id: str
    full_name: str
    skills: List[str]
    tasks: List[UserTask] = []


class TaskAssigneeMatchRequest(BaseModel):
    task_data: TaskData
    users: List[UserProfile]


class UserSuggestion(BaseModel):
    id: str
    reason: str


class TaskAssigneeMatchResponse(BaseModel):
    suggestions: List[UserSuggestion]


class TaskDescriptionRequest(BaseModel):
    title: str


class TaskDescriptionResponse(BaseModel):
    description: str


class TaskDurationRequest(BaseModel):
    title: str
    description: str
    assignee: Optional[UserProfile] = None  # Reusing existing UserProfile model


class TaskDurationResponse(BaseModel):
    duration: str  # e.g. "2 days", "4 hours"
    explanation: str  # Why this duration was suggested
