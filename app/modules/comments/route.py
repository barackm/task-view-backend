# modules/comments/route.py
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.modules.comments import service
from app.modules.comments.schema import CommentCreate, CommentUpdate, CommentResponse

router = APIRouter()

@router.post("/", response_model=CommentResponse)
def create_comment_endpoint(comment_data: CommentCreate, request: Request, db: Session = Depends(get_db)):
    current_user = request.state.user
    return service.create_comment(db, comment_data, current_user.id)

@router.get("/{task_id}", response_model=list[CommentResponse])
def get_comments_by_task_endpoint(task_id: int, db: Session = Depends(get_db)):
    return service.get_comments_by_task(db, task_id)

@router.put("/{comment_id}", response_model=CommentResponse)
def update_comment_endpoint(comment_id: int, comment_data: CommentUpdate, db: Session = Depends(get_db)):
    return service.update_comment(db, comment_id, comment_data)

@router.delete("/{comment_id}")
def delete_comment_endpoint(comment_id: int, db: Session = Depends(get_db),):
    return service.delete_comment(db, comment_id)
