from sqlalchemy.orm import Session
from app.db.models import Project
from .schema import ProjectCreate, ProjectUpdate
from typing import List

def create_project(db: Session, project_data: ProjectCreate, owner_id: int) -> Project:
    new_project = Project(
        name=project_data.name,
        description=project_data.description,
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
