from fastapi import APIRouter, Depends, HTTPException, status
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from .. import models
from ..schemas import SubjectCreate, SubjectResponse, User
from ..database import get_db
import psycopg2
from ..jwt import get_current_user

try:
    conn = psycopg2.connect(
        user='postgres',
        host='postgres',
        password=123,
        database='app',
        cursor_factory=RealDictCursor
    )

    conn.autocommit = True
except Exception as ex:
    print(ex)

router = APIRouter(tags=['subjects'])


@router.post('/subjects', response_model=SubjectResponse, status_code=status.HTTP_201_CREATED)
def create_subject(subject: SubjectCreate, db: Session = Depends(get_db)):
    if not subject.groups_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Вы не выбрали ни одной группы')
    groups = []
    for i in subject.groups_id:
        group = db.query(models.Group).filter(models.Group.id == i).first()
        if not group:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'продукта с id {i} нет')

        groups.append(group)
    new_subject = models.Subject(name_of_subject=subject.name_of_subject,
                                 groups=groups)

    db.add(new_subject)
    db.commit()
    db.refresh(new_subject)
    return new_subject


@router.get('/subjects', response_model=list[SubjectResponse])
def get_subjects(db: Session = Depends(get_db)):
    subjects = db.query(models.Subject).all()
    return subjects


@router.get('/subjects/my')
def get_subjects_my(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Возвращает subjects которые есть у студента
    """
    user = current_user.dict().get('id_student')
    with conn.cursor() as cursor:
        cursor.execute(
            '''
            select name_of_subject, subjects.id from subjects 
            join groups_subjects on groups_subjects.subject_id = subjects.id
            join groups on groups.id = groups_subjects.group_id
            join students on students.group_id = groups.id
            where students.id = %s
            ''', (user,)
        )
        subjects = cursor.fetchall()
        return subjects


@router.delete('/subjects/{subject_id}')
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    subject_query = db.query(models.Subject).filter(models.Subject.id == subject_id)
    subject = subject_query.first()
    if not subject:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')
    subject_query.delete()
    db.commit()
    return {'msg': 'успешно удалено'}
