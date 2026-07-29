from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session
import models,schemas,crud
from database import SessionLocal,engine
from fastapi.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind = engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
       "https://mini-student-project.netlify.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/students/", response_model=schemas.StudentResponse)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    print("sdtufjrn",student)
    db_student = crud.create_student(db, student)
    return db_student

@app.get("/students/", response_model=list[schemas.StudentResponse])
def read_all(db: Session = Depends(get_db)):
    students = crud.get_students(db)
    return students

@app.put("/students/{student_id}", response_model=schemas.StudentResponse)
def update_student(student_id: int,student: schemas.StudentUpdate,db: Session = Depends(get_db)):
    update_student= crud.search_students_by_id(db,student_id,student)
    if not update_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return update_student


@app.get("/students/search", response_model=list[schemas.StudentResponse])
def search_by_course(course: str, db:Session = Depends(get_db)):
    student_course= crud.search_students_by_course(db=db,course=course)
    if not student_course:
        raise HTTPException(status_code=404, detail="Student not found")
    return student_course


@app.delete("/students/{student_id}")
def delete(student_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_student(db, student_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}