
from sqlalchemy.orm import Session
import models, schemas

def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def get_students(db: Session):
    return db.query(models.Student).all()


def search_students_by_id(db:Session,student_id: int,student: schemas.StudentUpdate):
    db_student = db.query(models.Student).filter(models.Student.id == student_id ).first()
    if db_student:
        db_student.name = student.name
        db_student.email = student.email
        db_student.age = student.age
        db_student.course = student.course
        db.commit()
        db.refresh(db_student)
    return db_student

def search_students_by_course(db: Session, course: str):
    return db.query(models.Student).filter(models.Student.course == course).all()

def delete_student(db: Session, student_id: int):
    db_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if db_student:
        db.delete(db_student)
        db.commit()
    return db_student