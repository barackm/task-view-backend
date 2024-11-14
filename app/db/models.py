from sqlalchemy import Column, Integer, String, ForeignKey, Text, Enum, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum
import datetime

Base = declarative_base()

class TaskStatus(enum.Enum):
    PENDING = "Pending"
    IN_PROGRESS = "InProgress"
    COMPLETED = "Completed"

class TaskPriority(enum.Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

def utc_now():
     return datetime.datetime.now(datetime.timezone.utc)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    position = Column(String, nullable=True)
    skills = Column(Text, nullable=True)
    experience_level = Column(String, nullable=True) 
    created_at = Column(TIMESTAMP, default=utc_now)
    
    projects = relationship("Project", back_populates="owner")
    tasks = relationship("Task", back_populates="assigned_user")

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    created_at = Column(TIMESTAMP, default=utc_now)
    updated_at = Column(TIMESTAMP, default=utc_now, onupdate=utc_now)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    tags = Column(Text)
    
    owner = relationship("User", back_populates="projects")
    tasks = relationship("Task", back_populates="project")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING)
    priority = Column(Enum(TaskPriority), default=TaskPriority.MEDIUM)
    created_at = Column(TIMESTAMP, default=utc_now)
    updated_at = Column(TIMESTAMP, default=utc_now, onupdate=utc_now)
    assigned_to = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"))
    tags = Column(Text)
    
    assigned_user = relationship("User", back_populates="tasks")
    project = relationship("Project", back_populates="tasks")
    comments = relationship("Comment", back_populates="task", cascade="all, delete-orphan")
    history = relationship("TaskHistory", back_populates="task", cascade="all, delete-orphan")


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    
    task = relationship("Task", back_populates="comments")
    user = relationship("User")

class TaskHistory(Base):
    __tablename__ = "task_history"
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"))
    status = Column(Enum(TaskStatus), nullable=False)
    timestamp = Column(TIMESTAMP, default=utc_now)
    changed_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    
    task = relationship("Task", back_populates="history")
    user = relationship("User")
    