from fastapi import APIRouter,Depends, HTTPException, Path
from typing import Annotated
from sqlalchemy.orm import Session
from app.models import Users
from starlette import status
from app.schema import TodoRequest
from app.database import sessionLocal


router = APIRouter()



def get_db():
    db = sessionLocal()
    try: 
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/auth/", status_code=status.HTTP_200_OK)
async def get_users(db: db_dependency):
    return db.query(Users).all()
