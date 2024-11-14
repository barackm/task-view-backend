import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import datetime
from sqlalchemy.orm import Session
from app.db.models import Project, Task, TaskStatus, TaskPriority
from app.modules.projects.service import manage_tags_for_object
from app.db.database import get_db


def setup_ecommerce_project(db: Session):
    project = Project(
        name="E-Commerce Platform Development",
        description="A comprehensive project to develop a scalable e-commerce platform with features such as product catalog, shopping cart, order management, and payment integration.",
        created_at=datetime.datetime.now(datetime.timezone.utc),
        updated_at=datetime.datetime.now(datetime.timezone.utc)
    )
    db.add(project)
    db.commit()
    db.refresh(project)

    tasks_data = [
        {
            "title": "Set up frontend framework",
            "description": "Choose and configure a frontend framework such as React or Vue.",
            "status": TaskStatus.PENDING,
            "priority": TaskPriority.HIGH,
            "tags": ["Frontend", "React", "Setup"]
        },
        {
            "title": "Design product listing page",
            "description": "Create a responsive design for the product listing page.",
            "status": TaskStatus.PENDING,
            "priority": TaskPriority.MEDIUM,
            "tags": ["Frontend", "Design", "Responsive"]
        },
        {
            "title": "Implement authentication",
            "description": "Add user authentication with JWT and OAuth support.",
            "status": TaskStatus.PENDING,
            "priority": TaskPriority.HIGH,
            "tags": ["Backend", "Auth", "Security"]
        },
        {
            "title": "Set up CI/CD pipeline",
            "description": "Configure continuous integration and deployment using GitHub Actions.",
            "status": TaskStatus.PENDING,
            "priority": TaskPriority.MEDIUM,
            "tags": ["DevOps", "CI/CD", "GitHub Actions"]
        },
        {
            "title": "Develop shopping cart functionality",
            "description": "Allow users to add, edit, and remove items from their shopping cart.",
            "status": TaskStatus.PENDING,
            "priority": TaskPriority.HIGH,
            "tags": ["Backend", "Frontend", "Feature Development"]
        },
        {
            "title": "Optimize database queries",
            "description": "Improve performance of database queries, especially on the product and order tables.",
            "status": TaskStatus.PENDING,
            "priority": TaskPriority.MEDIUM,
            "tags": ["Backend", "Database", "Performance"]
        },
        {
            "title": "Implement payment gateway integration",
            "description": "Integrate payment processing with PayPal and Stripe.",
            "status": TaskStatus.PENDING,
            "priority": TaskPriority.HIGH,
            "tags": ["Backend", "Payments", "Integration"]
        },
        {
            "title": "Design admin dashboard",
            "description": "Create an admin dashboard for managing products, orders, and user accounts.",
            "status": TaskStatus.PENDING,
            "priority": TaskPriority.MEDIUM,
            "tags": ["Frontend", "Admin Panel", "Design"]
        },
        {
            "title": "Set up monitoring and logging",
            "description": "Implement monitoring with Prometheus and logging with ELK stack.",
            "status": TaskStatus.PENDING,
            "priority": TaskPriority.MEDIUM,
            "tags": ["DevOps", "Monitoring", "Logging"]
        }
    ]
  
    for task_data in tasks_data:
        task = Task(
            title=task_data["title"],
            description=task_data["description"],
            status=task_data["status"],
            priority=task_data["priority"],
            project_id=project.id,
            created_at=datetime.datetime.now(datetime.timezone.utc),
            updated_at=datetime.datetime.now(datetime.timezone.utc)
        )
        db.add(task)
        db.commit()
        db.refresh(task)

        for tag in task_data["tags"]:
            manage_tags_for_object(db, "task", task.id, tag, action="add")
            manage_tags_for_object(db, "project", project.id, tag, action="add")

    db.commit()
    print("E-commerce project setup with unassigned tasks and tags is complete.")

if __name__ == "__main__":
    db = next(get_db())
    try:
        setup_ecommerce_project(db)
    finally:
        db.close()
