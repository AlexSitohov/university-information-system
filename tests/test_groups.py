import sys

sys.path.append('uis/university-information-system-/app')
from app import main
from fastapi.testclient import TestClient
from fastapi import status

client = TestClient(main.app)


def test_get_groups():
    response = client.get('/groups')
    assert response.status_code == status.HTTP_200_OK


def test_post_groups():
    response = client.post('/groups')
    assert response.status_code == status.HTTP_201_CREATED

