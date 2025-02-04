from fastapi import APIRouter , Depends , HTTPException
from sqlalchemy.orm import Session 
from src.auth.utils import get_current_user
from src.base.db import get_db
from src.schemas.user import TeacherUpdate
from src.model import Student , User, Teacher
from typing import Optional


router = APIRouter()


@router.put("/update-teacher")
def update_question(
    teacher_item: TeacherUpdate,
    user_info: User = Depends(get_current_user),
    db : Session = Depends(get_db)
):
    

    teacher_info = db.query(Teacher).filter(Teacher.user_id == user_info.id).first()
    if not teacher_info:
            raise HTTPException(
                status_code=404 , 
                detail="Question not found"
            )
        
    update_data = teacher_item.dict(exclude_unset=True)
    for key , value in update_data.items():
        setattr(teacher_info , key, value)
    db.commit()
    db.refresh(teacher_info)
    return teacher_info