from fastapi import APIRouter , Depends , HTTPException
from sqlalchemy.orm import Session 
from src.base.db import get_db
from src.schemas.user import StudentUpdate
from src.model import Student


router = APIRouter()


@router.put("/update-student")
def update_question(
    student_id : int,
    question_item: StudentUpdate,
    db : Session = Depends(get_db)
):
    student = db.get(Student , student_id)
    if not student:
        raise HTTPException(
            status_code=404 , 
            detail="Question not found"
        )
    
    update_data = question_item.dict(exclude_unset=True)
    for key , value in update_data.items():
        setattr(student , key, value)
        
    db.commit()
    db.refresh(student)
    return Student