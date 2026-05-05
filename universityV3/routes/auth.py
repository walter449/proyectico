from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.user_model import UserRegister, UserVerify, UserLogin
from controllers.auth_controller import AuthController
from database import get_db

router = APIRouter(prefix="/auth")

@router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    return AuthController.register(user, db)

@router.post("/verify")
def verify(data: UserVerify, db: Session = Depends(get_db)):
    return AuthController.verify(data, db)

@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    return AuthController.login(data, db)
