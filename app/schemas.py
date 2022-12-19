from pydantic import BaseModel, Field
from datetime import datetime


class Group(BaseModel):
    id: int

    class Config:
        orm_mode = True


class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    age: int = Field(gt=15, lt=100)
    group_id: int

    class Config:
        orm_mode = True


class StudentResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    age: int = Field(gt=15, lt=100)
    group_id: int

    class Config:
        orm_mode = True


class SubjectCreate(BaseModel):
    name_of_subject: str
    groups_id: list[int]

    class Config:
        orm_mode = True


class SubjectResponse(BaseModel):
    id: int
    name_of_subject: str
    groups: list[Group]

    class Config:
        orm_mode = True


class ClassCreate(BaseModel):
    task: str
    date_time: datetime
    group_id: int
    subject_id: int

    class Config:
        orm_mode = True


class ClassResponse(BaseModel):
    id: int
    task: str
    date_time: datetime
    group_id: int
    subject_id: int

    class Config:
        orm_mode = True


class Rating(BaseModel):
    student_id: int
    class_id: int
    value: int = Field(gt=0, lt=6)

    class Config:
        orm_mode = True


class User(BaseModel):
    username: str
    password: str
    student_id: int

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    id_user: int
    is_staff: bool
    id_student: int

