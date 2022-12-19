from fastapi import APIRouter, Depends, HTTPException, status

from .. import models
from ..database import get_db
from sqlalchemy.orm import Session
from ..hash import verify_password
from ..jwt import create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=['authentication'])


@router.post('/login', status_code=status.HTTP_200_OK)
def login(login_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.username == login_data.username)
    user = user_query.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='invalid username')
    if not verify_password(login_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='invalid password')
    access_token = create_access_token(data={'id_user': user.id,
                                             'id_student': user.student_id,
                                             'is_staff': user.is_staff})
    return {"access_token": access_token, "token_type": "bearer"}
