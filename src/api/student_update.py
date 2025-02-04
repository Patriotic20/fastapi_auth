from fastapi import APIRouter , Depends , HTTPException
from sqlalchemy.orm import Session 
from src.auth.utils import get_current_user
from src.base.db import get_db
from src.schemas.user import StudentUpdate 
from src.model import Student , User



router = APIRouter()


@router.put("/update-student")
def update_question(
    student_item: StudentUpdate,
    user_info: User = Depends(get_current_user),
    db : Session = Depends(get_db)
):
    

    student_info = db.query(Student).filter(Student.user_id == user_info.id).first()
    if not student_info:
            raise HTTPException(
                status_code=404 , 
                detail="Student not found"
            )
        
    update_data = student_item.dict(exclude_unset=True)
    for key , value in update_data.items():
        setattr(student_info , key, value)
    db.commit()
    db.refresh(student_info)
    return student_info