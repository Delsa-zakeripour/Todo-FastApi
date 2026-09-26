from fastapi import status
from fastapi.testclient import TestClient

from app.router.auth import get_current_user
from app.router.admin import get_db
from .utils import *
from app.main import app


app.dependency_overrides[get_db] = overide_get_db
app.dependency_overrides[get_current_user] = overide_get_current_user

client = TestClient(app)


def test_admin_reed_all_authentication(test_todo):
    response = client.get('/admin/todos')
    assert response.status_code == status.HTTP_200_OK 
    assert response.json() == [{
    "complete": True,
    "title": "running",
    "description": "for race",
     "priority": 7,
    "id": 1,
    "owner_id": 7
  }]



def test_admin_delete(test_todo):
    response = client.delete('/admin/todo/1')
    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None    