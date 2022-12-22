from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models
from ..schemas import ClassCreate, ClassResponse
from ..database import get_db

router = APIRouter(tags=['classes'])


@router.post('/classes', response_model=ClassResponse, status_code=status.HTTP_201_CREATED)
def create_class(_class: ClassCreate, db: Session = Depends(get_db)):
    new_class = models.Class(**_class.dict())
    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    return new_class


@router.get('/classes', response_model=list[ClassResponse])
def get_classes(db: Session = Depends(get_db)):
    classes = db.query(models.Class).all()
    return classes


@router.delete('/classes/{_class_id}')
def delete_class(_class_id: int, db: Session = Depends(get_db)):
    class_query = db.query(models.Class).filter(models.Class.id == _class_id)
    _class = class_query.first()
    if not _class:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')
    class_query.delete()
    db.commit()
    return {'msg': 'успешно удалено'}
