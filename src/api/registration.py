from fastapi import APIRouter, Depends, HTTPException, status
from src.schemas.user import RegisterRequest
from sqlalchemy.orm import Session
from src.base.db import get_db
from src.model.user import User, UserRole
from src.auth.utils import hash_password

router = APIRouter()

@router.post("/register")
def register(user_data: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter((User.username == user_data.username)).first()
    
    if existing_user:
        if existing_user.username == user_data.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    new_user = User(
    username=user_data.username,
    hashed_password=hash_password(user_data.password),
    disabled=False,
    role = UserRole.student.value
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully"}