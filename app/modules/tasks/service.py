from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.db.models import Task, User
from .schema import TaskCreate, TaskUpdate, TaskStatus, TaskPriority
from app.db.models import Project
from datetime import datetime
from typing import List, Optional

def create_task(db: Session, task_data: TaskCreate) -> Task:
    project = db.query(Project).filter(Project.id == task_data.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    new_task = Task(**task_data.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def get_task(db: Session, task_id: int) -> Task:
    return db.query(Task).filter(Task.id == task_id).first()

def get_tasks(db: Session, project_id: int) -> list[Task]:
    return db.query(Task).filter(Task.project_id == project_id).all()

def update_task(db: Session, task_id: int, task_data: TaskUpdate) -> Task:
    task = get_task(db, task_id)
    if task:
        for key, value in task_data.dict(exclude_unset=True).items():
            setattr(task, key, value)
        db.commit()
        db.refresh(task)
    return task

def delete_task(db: Session, task_id: int) -> bool:
    task = get_task(db, task_id)
    if task:
        db.delete(task)
        db.commit()
        return True
    return False

def assign_task_to_user(db: Session, task_id: int, user_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    task.assigned_to = user_id
    db.commit()
    db.refresh(task)
    return task


def get_tasks_for_user(db: Session, user_id: int) -> List[Task]:
    return db.query(Task).filter(Task.assigned_to == user_id).all()

def search_tasks(
    db: Session,
    title: Optional[str] = None,
    description: Optional[str] = None,
    statuses: Optional[List[str]] = None,
    priorities: Optional[List[str]] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    assignee_ids: Optional[List[int]] = None
) -> List[Task]:
    query = db.query(Task)

    if title:
        query = query.filter(Task.title.ilike(f"%{title}%"))
    if description:
        query = query.filter(Task.description.ilike(f"%{description}%"))

    if statuses:
        status_enums = [TaskStatus(status) for status in statuses]
        query = query.filter(Task.status.in_(status_enums))

    if priorities:
        priority_enums = [TaskPriority(priority) for priority in priorities]
        query = query.filter(Task.priority.in_(priority_enums))
        
    if assignee_ids:
        query = query.filter(Task.assigned_to.in_(assignee_ids))

    if date_from:
        query = query.filter(Task.created_at >= date_from)
    if date_to:
        query = query.filter(Task.created_at <= date_to)

    return query.all()