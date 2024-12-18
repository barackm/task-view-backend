from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models import User
from .schema import ProjectCreate, ProjectUpdate, ProjectResponse, TagRequest
from .service import create_project, get_project, get_all_projects, update_project, delete_project, manage_tags_for_object
from typing import List

router = APIRouter()

@router.get("/", response_model=List[ProjectResponse])
def read_projects(
    request: Request,
    db: Session = Depends(get_db),
):
    current_user: User = request.state.user
    return get_all_projects(db, current_user.id)

@router.get("/{project_id}", response_model=ProjectResponse)
def read_project(
    request: Request,
    project_id: int,
    db: Session = Depends(get_db),
):
    current_user: User = request.state.user
    project = get_project(db, project_id)
    if not project or project.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project_endpoint(
    project_data: ProjectCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    current_user: User = request.state.user
    return create_project(db, project_data, current_user.id)


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project_endpoint(
    project_id: int,
    project_data: ProjectUpdate,
    request: Request,
    db: Session = Depends(get_db),
):
    current_user: User = request.state.user
    project = get_project(db, project_id)
    if not project or project.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return update_project(db, project_id, project_data)

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project_endpoint(
    project_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    current_user: User = request.state.user
    project = get_project(db, project_id)
    if not project or project.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    if not delete_project(db, project_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to delete project")


@router.post("/{item_type}/{item_id}/tags")
def manage_tags_endpoint(
    item_type: str,
    item_id: int,
    tag_request: TagRequest,
    db: Session = Depends(get_db)
):
    try:
        obj = manage_tags_for_object(
            db=db,
            item_type=item_type,
            obj_id=item_id,
            tag=tag_request.tag,
            action=tag_request.action
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return obj.tags.split(",") if obj.tags else []