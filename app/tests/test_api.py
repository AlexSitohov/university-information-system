from .. import main
from fastapi import status, Depends, FastAPI
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from ..database import Base, get_db
from datetime import datetime

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:123@test_postgres/test_app'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


main.app.dependency_overrides[get_db] = override_get_db

Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client():
    Base.metadata.create_all(bind=engine)
    yield TestClient(main.app)


def test_post_groups(client):
    response = client.post('/groups')
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json().get('id') == 1


def test_get_groups(client):
    response = client.get('/groups')
    assert response.status_code == status.HTTP_200_OK


def test_create_student(client):
    response = client.post('/students', json={"first_name": "Alexander", "last_name": "Merc", "age": 22, "group_id": 1})
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json().get("first_name") == "Alexander"


def test_get_student(client):
    response = client.get('/students/1')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": 1,
        "first_name": "Alexander",
        "last_name": "Merc",
        "age": 22,
        "group_id": 1
    }


def test_create_subject(client):
    response = client.post('/subjects', json={
        "name_of_subject": "python",
        "groups_id": [
            1
        ]
    })
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "id": 1,
        "name_of_subject": "python",
        "groups": [
            {
                "id": 1
            }
        ]
    }


def test_get_subjects(client):
    response = client.get('/subjects')
    assert response.status_code == status.HTTP_200_OK


def test_create_class(client):
    response = client.post('/classes', json={
        "task": "python start",
        "date_time": str(datetime.now()),
        "group_id": 1,
        "subject_id": 1
    })
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json().get('task') == 'python start'


def test_get_classes(client):
    response = client.get('/subjects')
    assert response.status_code == status.HTTP_200_OK


def test_create_rating(client):
    response = client.post('/ratings', json={
        "student_id": 1,
        "class_id": 1,
        "value": 5
    })
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "student_id": 1,
        "class_id": 1,
        "value": 5
    }


def test_registration(client):
    response = client.post('/users', json={
        "username": "Alexander",
        "password": "123",
        "student_id": 1
    })
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json().get("username") == "Alexander"


def test_get_users(client):
    response = client.get('/users')
    assert response.status_code == status.HTTP_200_OK
