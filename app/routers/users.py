from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models
from ..schemas import User
from ..database import get_db
from ..hash import hash

router = APIRouter(tags=['users'])


@router.post('/users')
def registration(user: User, db: Session = Depends(get_db)):
    hashed_password = hash(user.password)
    new_user = models.User(username=user.username, password=hashed_password, student_id=user.student_id)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/users')
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.delete('/users/{user_id}')
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == user_id)
    user = user_query.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')
    user_query.delete()
    db.commit()
    return {'msg': 'успешно удалено'}
