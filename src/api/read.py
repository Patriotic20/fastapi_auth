from fastapi import APIRouter, Depends
from src.schemas.user import UserResponse
from src.auth.utils import get_user_role
from src.model.user import UserRole


router = APIRouter()

@router.get("/users/me")
def read_users_me(current_user: UserResponse = Depends(get_user_role(UserRole.student))):
    return current_user