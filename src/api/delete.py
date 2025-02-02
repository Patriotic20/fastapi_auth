from fastapi import APIRouter, Depends
from src.base.db import get_db
from sqlalchemy.orm import Session
from src.model.user import User

router = APIRouter()

@router.delete("/delete")
def delete(user_id: int , db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    db.delete(user)
    db.commit()
    return "delete"