from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.db.models import Task, User
from .schema import TaskCreate, TaskUpdate
from app.db.models import Project

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