from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from .schema import TaskCreate, TaskUpdate, TaskResponse, TaskAssign, TaskSearchSchema
from .service import create_task, get_task, get_tasks, update_task, delete_task, assign_task_to_user, get_tasks_for_user, search_tasks
from typing import List

router = APIRouter()

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task_endpoint(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
):
    return create_task(db, task_data)

@router.get("/{task_id}", response_model=TaskResponse)
def read_task(
    task_id: int,
    db: Session = Depends(get_db),
):
    task = get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@router.get("/user/{user_id}/tasks", response_model=List[TaskResponse])
def get_tasks_for_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    return get_tasks_for_user(db, user_id)

@router.get("/", response_model=List[TaskResponse])
def read_tasks(
    project_id: int,
    db: Session = Depends(get_db),
):
    return get_tasks(db, project_id)

@router.put("/{task_id}", response_model=TaskResponse)
def update_task_endpoint(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db),
):
    task = update_task(db, task_id, task_data)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_endpoint(
    task_id: int,
    db: Session = Depends(get_db),
):
    if not delete_task(db, task_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

@router.put("/{task_id}/assign", response_model=TaskResponse)
def assign_task_endpoint(task_id: int, assignment: TaskAssign, db: Session = Depends(get_db)):
    print(assignment, "assignment", task_id)
    return assign_task_to_user(db, task_id, assignment.user_id)


@router.post("/tasks/search")
def search_tasks_endpoint(
    search_criteria: TaskSearchSchema,
    db: Session = Depends(get_db),
):
    results = search_tasks(
        db=db,
        title=search_criteria.title,
        description=search_criteria.description,
        statuses=search_criteria.statuses,
        priorities=search_criteria.priorities,
        date_from=search_criteria.date_from,
        date_to=search_criteria.date_to,
        assignee_ids=search_criteria.assignee_ids
    )

    return results
