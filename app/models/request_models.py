from pydantic import BaseModel
from typing import List, Optional

class Skill(BaseModel):
    name: str
    level: Optional[str] = "Intermediate"

class TaskData(BaseModel):
    title: str
    description: str
    required_skills: List[Skill]
    deadline: Optional[str]
    priority: Optional[str] = "Medium"

class UserProfile(BaseModel):
    id: str
    full_name: str
    skills: List[Skill]
    availability: Optional[str]
    current_workload: Optional[int]

class TaskAssigneeMatchRequest(BaseModel):
    task_data: TaskData
    users: List[UserProfile]
