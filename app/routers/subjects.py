from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models
from ..schemas import SubjectCreate, SubjectResponse
from ..database import get_db

router = APIRouter(tags=['subjects'])


@router.post('/subjects', response_model=SubjectResponse, status_code=status.HTTP_201_CREATED)
def create_group(subject: SubjectCreate, db: Session = Depends(get_db)):
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


@router.delete('/subjects/{subject_id}')
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    subject_query = db.query(models.Subject).filter(models.Subject.id == subject_id)
    subject = subject_query.first()
    if not subject:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')
    subject_query.delete()
    db.commit()
    return {'msg': 'успешно удалено'}
