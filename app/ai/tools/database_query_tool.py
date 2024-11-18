from typing import Any, Dict, List
from sqlalchemy.orm import Session
from app.db.models import Task, User, Project


class DatabaseQueryTool:
    """Custom tool for querying the database."""

    def __init__(self, db: Session):
        """Initialize the tool with the database session."""
        self.db = db
        
    def fetch_users(self) -> List[Dict[str, Any]]:
        """Fetch all users from the database."""
        users = self.db.query(User).all()
        return [{"id": user.id, "name": user.name, "email": user.email, "skills": user.skills, "position": user.position} for user in users]
    
    def __repr__(self):
        return f"<DatabaseQueryTool connected to {self.db.bind.url.database}>"