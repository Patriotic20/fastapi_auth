from fastapi import APIRouter, Depends, HTTPException, status
from src.base.db import get_db
from sqlalchemy.orm import Session
from src.model import Student , Teacher
from src.model.user import User

router = APIRouter()

@router.delete("/delete")
def delete(user_id: int , db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user.role == "student":        
        student = db.query(Student).filter(Student.user_id == user_id).first()
        db.delete(student)
    if user.role == "teacher":
        teacher = db.query(Teacher).filter(Teacher.user_id == user_id).first()
        db.delete(teacher)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    db.delete(user)
    db.commit()
    return "delete"