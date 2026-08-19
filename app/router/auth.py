from fastapi import APIRouter,Depends, HTTPException, Path
from typing import Annotated
from sqlalchemy.orm import Session
from app.models import Users
from starlette import status
from app.schema import CreateUserRequest
from app.database import sessionLocal


router = APIRouter()



def get_db():
    db = sessionLocal()
    try: 
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/auth")
async def create_user(create_user_request: CreateUserRequest):
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=create_user_request. password,
        is_active=True,
    )

    return create_user_model