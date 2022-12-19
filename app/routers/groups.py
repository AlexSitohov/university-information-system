from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models
from ..schemas import Group
from ..database import get_db

router = APIRouter(tags=['groups'])


@router.post('/groups', response_model=Group, status_code=status.HTTP_201_CREATED)
def create_group(db: Session = Depends(get_db)):
    new_group = models.Group()
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    return new_group


@router.get('/groups')
def get_groups(db: Session = Depends(get_db)):
    groups = db.query(models.Group).all()
    return groups


@router.delete('/groups/{group_id}')
def delete_group(group_id: int, db: Session = Depends(get_db)):
    group_query = db.query(models.Group).filter(models.Group.id == group_id)
    group = group_query.first()
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')
    group_query.delete()
    db.commit()
    return {'msg': 'успешно удалено'}
