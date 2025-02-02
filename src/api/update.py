from fastapi import APIRouter, Depends, HTTPException, status
from src.base.db import get_db
from typing import Union
from sqlalchemy.orm import Session
from src.model import Student , Teacher , User
from src.auth.utils import get_current_user
from src.schemas.user import StudentUpdate, TeacherUpdate
from pydantic import BaseModel



router = APIRouter()

role_model_map = {
    "student": (Student , StudentUpdate),
    "teacher": (Teacher , TeacherUpdate),
}

@router.put("/update")
def update_question(
    user_info : User = Depends(get_current_user),
    db : Session = Depends(get_db),
    user_update : Union[StudentUpdate, TeacherUpdate] = None,
):
    if user_info.role not in role_model_map:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unauthorized role"
        )
        
    model_class , schemas_class = role_model_map[user_info.role]
    
    user = db.get(model_class , user_info.id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
        
    update_data = schemas_class.model_validate(user_update).model_dump(exclude_unset=True)

    
    for key , value in update_data.items():
        setattr(user, key, value)
        
        
    db.commit()
    db.refresh(user)
    return user
    ...