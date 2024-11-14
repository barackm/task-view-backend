from sqlalchemy.orm import Session
from app.db.models import Project, Task
from .schema import ProjectCreate, ProjectUpdate
from typing import List

def create_project(db: Session, project_data: ProjectCreate, owner_id: int) -> Project:
    tags = ",".join(project_data.tags) if project_data.tags else None
    new_project = Project(
        name=project_data.name,
        description=project_data.description,
        tags=tags,
        owner_id=owner_id
    )
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

def get_project(db: Session, project_id: int) -> Project:
    return db.query(Project).filter(Project.id == project_id).first()

def get_all_projects(db: Session, owner_id: int) -> List[Project]:
    return db.query(Project).filter(Project.owner_id == owner_id).all()

def update_project(db: Session, project_id: int, project_data: ProjectUpdate) -> Project:
    project = db.query(Project).filter(Project.id == project_id).first()
    if project:
        for key, value in project_data.dict(exclude_unset=True).items():
            setattr(project, key, value)
        db.commit()
        db.refresh(project)
    return project

def delete_project(db: Session, project_id: int) -> bool:
    project = db.query(Project).filter(Project.id == project_id).first()
    if project:
        db.delete(project)
        db.commit()
        return True
    return False

def manage_tags_for_object(
    db: Session, item_type: str, obj_id: int, tag: str, action: str
):
    if item_type not in ["project", "task"]:
        raise ValueError("Invalid item type. Only 'project' and 'task' are supported.")

    obj = db.query(Project if item_type == "project" else Task).get(obj_id)
    if not obj:
        raise ValueError("Item not found.")

    tags = set(obj.tags.split(",")) if obj.tags else set()
    if action == "add":
        tags.add(tag)
    elif action == "remove" and tag in tags:
        tags.remove(tag)
    else:
        raise ValueError("Invalid action or tag not found in item.")

    obj.tags = ",".join(tags)
    db.commit()
    db.refresh(obj)
    return obj