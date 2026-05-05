import random
import hashlib
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models.user_model import UserRegister, UserVerify, UserLogin
from models.user_db_model import User
from email_service import send_otp_email

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def generate_otp() -> str:
    return str(random.randint(100000, 999999))

class AuthController:

    @staticmethod
    def register(user: UserRegister, db: Session):
        existing = db.query(User).filter(User.email == user.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="El correo ya está registrado")

        otp = generate_otp()
        new_user = User(
            email=user.email,
            password=hash_password(user.password),
            otp_code=otp,
            verified=False
        )
        db.add(new_user)
        db.commit()

        send_otp_email(user.email, otp)
        return {"message": "Código de verificación enviado al correo"}

    @staticmethod
    def verify(data: UserVerify, db: Session):
        user = db.query(User).filter(User.email == data.email).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        if user.otp_code != data.otp_code:
            raise HTTPException(status_code=400, detail="Código incorrecto")

        user.verified = True
        user.otp_code = None
        db.commit()
        return {"message": "Cuenta verificada correctamente"}

    @staticmethod
    def login(data: UserLogin, db: Session):
        user = db.query(User).filter(User.email == data.email).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        if not user.verified:
            raise HTTPException(status_code=403, detail="Cuenta no verificada")
        if user.password != hash_password(data.password):
            raise HTTPException(status_code=401, detail="Contraseña incorrecta")

        return {"message": "Login exitoso", "email": user.email}
