from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.db.models import Comment, Task
from app.modules.comments.schema import CommentCreate, CommentUpdate

def create_comment(db: Session, comment_data: CommentCreate, user_id: int):
    task = db.query(Task).filter(Task.id == comment_data.task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    
    new_comment = Comment(
        task_id=comment_data.task_id,
        user_id=user_id,
        content=comment_data.content
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

def get_comments_by_task(db: Session, task_id: int):
    return db.query(Comment).filter(Comment.task_id == task_id).all()

def update_comment(db: Session, comment_id: int, comment_data: CommentUpdate):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found",
        )
    
    if comment_data.content is not None:
        comment.content = comment_data.content
    
    db.commit()
    db.refresh(comment)
    return comment

def delete_comment(db: Session, comment_id: int):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found",
        )
    
    db.delete(comment)
    db.commit()
    return comment
