from fastapi import APIRouter,Depends, HTTPException, Path
from datetime import datetime, timedelta, timezone
from typing import Annotated
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.models import Users
from starlette import status
from app.schema import CreateUserRequest
from app.database import sessionLocal
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

router = APIRouter(prefix='/auth',tags=['auth'])


SECRET_KEY = '7eeb5ae829a4a6437907e026a90433acb9d8be1940cc22607d37e6e272d80467'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

class Token(BaseModel):
    access_token: str
    token_type: str 

 
def get_db():
    db = sessionLocal()
    try: 
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

def authentication_user(username: str, password: str, db):
    User = db.query(Users).filter(Users.username == username).first()
    if not User:
        return False
    if not bcrypt_context.verify(password, User.hashed_password):
        return False

    return User



def  create_access_token(username:str, user_id: int, role: str, expire_delta: timedelta):
    encode = {'sub': username, 'id': user_id, 'role': role}
    expires = datetime.now(timezone.utc) + expire_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, ALGORITHM) 


def  get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload= jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("payloaddddd",payload)
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get("role")
        if username is None or user_id is None: 
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user.')
        return {'username': username, 'id': user_id, "role": user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")

      

@router.post("/")
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username, 
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True,
        phone_number=create_user_request.phone_number
    )
 
    db.add(create_user_model)
    db.commit()




@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authentication_user(form_data.username, form_data.password, db)
    if not user   :
        return 'Failed Authentication'     
    token  = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))
    # return 'Successful Authentication'
    # return token
    return {'access_token': token, 'token_type': 'bearer'}