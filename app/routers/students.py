from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models
from ..schemas import StudentCreate, StudentResponse
from ..database import get_db

router = APIRouter(tags=['students'])


@router.post('/students', response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    new_student = models.Student(**student.dict())
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student


@router.get('/students', response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    students = db.query(models.Student).all()
    return students


@router.get('/students/{student_id}')
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')
    return student


@router.delete('/students/{student_id}')
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student_query = db.query(models.Student).filter(models.Student.id == student_id)
    student = student_query.first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')
    student_query.delete()
    db.commit()
    return {'msg': 'успешно удалено'}
