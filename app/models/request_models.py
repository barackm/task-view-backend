from pydantic import BaseModel
from typing import List


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
