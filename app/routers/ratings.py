from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models
from ..schemas import Rating, User
from ..database import get_db
from ..jwt import get_current_user

router = APIRouter(tags=['ratings'])


@router.post('/ratings', response_model=Rating, status_code=status.HTTP_201_CREATED)
def create_group(rating: Rating, db: Session = Depends(get_db)):
    new_rating = models.Rating(**rating.dict())
    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)
    return new_rating


@router.get('/ratings', response_model=list[Rating])
def get_ratings(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    ratings = db.query(models.Rating).filter(models.Rating.student_id == current_user.dict().get('id_student')).all()
    return ratings


@router.delete('/ratings/{rating_id}')
def delete_rating(rating_id: int, db: Session = Depends(get_db)):
    rating_query = db.query(models.Rating).filter(models.Rating.id == rating_id)
    rating = rating_query.first()
    if not rating:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')
    rating_query.delete()
    db.commit()
    return {'msg': 'успешно удалено'}
