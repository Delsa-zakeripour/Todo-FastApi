from .utils import *
from app.router.users import get_db, get_current_user
from fastapi import status
from fastapi.testclient import TestClient
from app.main import app

from app.models import Todos, Users



app.dependency_overrides[get_db] = overide_get_db
app.dependency_overrides[get_current_user] = overide_get_current_user

client = TestClient(app)


def test_return_user(test_user):
    response = client.get('/user')
    assert response.status_code == status.HTTP_200_OK 
    assert response.json()['username'] == 'firsttest'
    assert response.json()['email'] == 'firsttest@gmail.com'
    assert response.json()['last_name'] == 'test'
    assert response.json()['is_active'] == True
    assert response.json()['phone_number'] == '12121212'
    assert response.json()['first_name'] == 'first'
    assert response.json()['first_name'] == 'first'
    assert response.json()['role'] == 'admin'



