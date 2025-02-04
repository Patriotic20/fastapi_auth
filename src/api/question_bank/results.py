from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from src.base.db import get_db
from src.model import Question, Student, User
from src.auth.utils import get_current_user

router = APIRouter()

@router.get("/test-check")
def check_test(
    user_id: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    student = db.query(Student).filter(Student.id == user_id.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="User not found")

    if not student.quiz_result or not isinstance(student.quiz_result, dict):
        raise HTTPException(status_code=400, detail="Invalid or missing quiz result")

    quiz_result = student.quiz_result  
    question_texts = list(quiz_result.keys())

    
    question_query = db.execute(select(Question).where(Question.text.in_(question_texts)))
    questions = {q.text: q.A for q in question_query.scalars().all()}


    correct_count = sum(1 for q_text, answer in quiz_result.items() if questions.get(q_text) == answer)
    incorrect_count = len(quiz_result) - correct_count


    student.correct_answers = correct_count
    student.incorrect_answers = incorrect_count

    db.commit()
    db.refresh(student)
    return student
