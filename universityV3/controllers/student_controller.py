from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from models.student_model import Student
from models.db_model import Student as StudentDB
from database import get_db

class StudentController:
    @staticmethod
    def get_all(db: Session) -> list[dict]:
        return db.query(StudentDB).all()

    @staticmethod
    def get_by_id(student_id: int, db: Session) -> dict:
        student = db.query(StudentDB).filter(StudentDB.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Estudiante no encontrado")
        return student

    @staticmethod
    def create(student: Student, db: Session):
        new_student = StudentDB(**student.model_dump())
        db.add(new_student)
        db.commit()
        db.refresh(new_student)
        return new_student

    @staticmethod
    def update(student_id: int, student: Student, db: Session):
        existing = db.query(StudentDB).filter(StudentDB.id == student_id).first()
        if not existing:
            raise HTTPException(status_code=404, detail="Estudiante no encontrado")
        for key, value in student.model_dump().items():
            setattr(existing, key, value)
        db.commit()
        db.refresh(existing)
        return existing

    @staticmethod
    def delete(student_id: int, db: Session):
        existing = db.query(StudentDB).filter(StudentDB.id == student_id).first()
        if not existing:
            raise HTTPException(status_code=404, detail="Estudiante no encontrado")
        db.delete(existing)
        db.commit()
        return {"message": "Estudiante eliminado correctamente"}
