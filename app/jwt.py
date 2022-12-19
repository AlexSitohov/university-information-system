from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from datetime import datetime, timedelta

from starlette import status

from . import schemas
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", scheme_name="JWT")


def create_access_token(data: dict):
    to_ecode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_ecode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_ecode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_user: int = payload.get('id_user')
        is_staff: bool = payload.get('is_staff')
        id_student: int = payload.get('id_student')
        if id_user is None:
            raise credentials_exception
        token_data = schemas.TokenData(id_user=id_user, is_staff=is_staff, id_student=id_student)
    except JWTError:
        raise credentials_exception
    return token_data


def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(data, credentials_exception)
