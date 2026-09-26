# from sqlalchemy import create_engine, text
# from sqlalchemy import StaticPool
# from sqlalchemy.orm import sessionmaker
# from app.database import Base
from app.main import app
from sqlalchemy import text
from app.router.todos import get_db, get_current_user
from fastapi.testclient import TestClient
from fastapi import status
from app.models import Todos
import pytest
from .utils import *
 

# SQLALCHEMY_DATABASE_URL = 'sqlite:///./testdb.db'

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL,
#     connect_args={'check_same_thread': False},
#     poolclass = StaticPool,

# )


# TestingSessionLocal = sessionmaker(autocommit= False, autoflush= False, bind= engine)
# Base.metadata.create_all(bind=engine)

# def overide_get_db():
#     db = TestingSessionLocal()
#     try:   
#         yield db
#     finally:
#         db.close() 


# def overide_get_current_user():
#     return {'username': 'firsttest', 'id': 7, 'user_role': 'admin'}


app.dependency_overrides[get_db] = overide_get_db
app.dependency_overrides[get_current_user] = overide_get_current_user


client = TestClient(app)




def test_read_all_authenticated(test_todo):
    response = client.get("/todo")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [  {
    "complete": True,
    "title": "running",
    "description": "for race",
    "id": 1,
    "priority": 7,
    "owner_id": 7
  }]



def test_read_one_authenticated(test_todo):
    response = client.get("/todo/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
    "complete": True,
    "title": "running",
    "description": "for race",
    "id": 1,
    "priority": 7,
    "owner_id": 7
  }



def test_read_one_authenticated_not_found():
    response = client.get("/todo/todo/3388") 
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found.'}



def test_create_todo(test_todo):
    request_data={
        "title": "string",
        "description": "string",
        "priority": 1,
        "complete": True
    } 

    response = client.post('/todo/todo', json=request_data)
    assert response.status_code == 201

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete') 



def test_update_todo(test_todo):
    request_data={
        'title':'change the title!',
        'description':"change the description",
        'priority':5,
        "complete": False         
    }

    response = client.put('/todo/todo/1', json=request_data)
    assert response.status_code == 202
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == 'change the title!'




def test_update_todo_not_found():
    request_data={
        'title':'change the title!',
        'description':"change the description",
        'priority':5,
        "complete": False         
    }

    response = client.put('/todo/todo/333', json=request_data)
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found.'}



def test_delete_todo(test_todo):
    response = client.delete('/todo/todo/1')
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None




def test_delete_todo_not_model():
    response = client.delete('/todo/todo/333')
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found.'}