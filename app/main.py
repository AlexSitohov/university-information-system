from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .database import Base
from .routers import groups, students, subjects, classes, ratings, users, authentication

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(groups.router)
app.include_router(students.router)
app.include_router(subjects.router)
app.include_router(classes.router)
app.include_router(ratings.router)
app.include_router(users.router)
app.include_router(authentication.router)

Base.metadata.create_all(engine)
