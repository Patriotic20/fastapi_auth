from fastapi import APIRouter , Depends , Response , Request , HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from src.model.user import User
from src.base.db import get_db
from src.auth.utils import authenticate_user , create_access_token, create_refresh_token, verify_token , get_user
from datetime import timedelta
from src.base.config import settings

router = APIRouter()

@router.post("/login")
def login(response : Response, form_data: OAuth2PasswordRequestForm = Depends() , db: Session = Depends(get_db)):
    user = authenticate_user(db , form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username and password"
        )
    access_token = create_access_token({"sub": user.username}, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_refresh_token({"sub": user.username}, timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))
    
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, samesite="lax", secure=True)
    
    return{"access_token": access_token, "token_type": "bearer"}

