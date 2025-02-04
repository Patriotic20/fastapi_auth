from fastapi import APIRouter
from .login import router as login
from .read import router as read
from .refresh import router as refresh
from .logout import router as logout
from .registration import router as registration
from .delete import router as delete
from .student_update import router as studnet_update
from .teacher_update import router as teacher_update
from .question_bank import router as question_bank

router = APIRouter()

router.include_router(logout)
router.include_router(read)
router.include_router(login)
router.include_router(refresh)
router.include_router(registration)
router.include_router(delete)
router.include_router(studnet_update)
router.include_router(teacher_update)
router.include_router(question_bank)


