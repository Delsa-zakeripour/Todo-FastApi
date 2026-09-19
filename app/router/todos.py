from fastapi import APIRouter,Depends, HTTPException, Path
from typing import Annotated
from sqlalchemy.orm import Session
from app.models import Todos
from starlette import status
from app.schema import TodoRequest
from app.database import sessionLocal
from app.router.auth import get_current_user 

router = APIRouter(prefix='/todo',tags=['todo'])


def get_db():
    db = sessionLocal()
    try: 
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)] 
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/",status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency,db: db_dependency):
    if user is None:
            raise HTTPException(status_code=401, detail="Authentication Failed.")
    return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency,user: user_dependency ,todo_id: int = Path(gt=0)):
    if user is None:
            raise HTTPException(status_code=401, detail="Authentication Failed.")
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail='Todo not found.')



@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest):

    if user is None: 
        raise HTTPException(status_code=401, detail="Authentication Failed.")
    todo_model = Todos(**todo_request.dict(), owner_id = user.get('id'))

    db.add(todo_model)
    db.commit()


@router.put('/todo/{todo_id}', status_code=status.HTTP_202_ACCEPTED)
async def update_todo(db: db_dependency, user: user_dependency, todo_rquest:TodoRequest, todo_id: int = Path(gt=0)):


    if user is None:
                raise HTTPException(status_code=401, detail="Authentication Failed.")
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not faound.')

    todo_model.title = todo_rquest.title
    todo_model.description = todo_rquest.description
    todo_model.priority = todo_rquest.priority
    todo_model.complete = todo_rquest.complete

    db.add(todo_model)
    db.commit()



@router.delete('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):  
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed.")
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='user not found.')
    db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).delete()

    db.commit()    