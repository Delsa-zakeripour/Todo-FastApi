
from sqlalchemy import create_engine, text
from sqlalchemy import StaticPool
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models import Todos, Users
import pytest
from app.router.auth import bcrypt_context

SQLALCHEMY_DATABASE_URL = 'sqlite:///./testdb.db'
 
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False},
    poolclass = StaticPool,

)


TestingSessionLocal = sessionmaker(autocommit= False, autoflush= False, bind= engine)
Base.metadata.create_all(bind=engine)

def overide_get_db():
    db = TestingSessionLocal()
    try:   
        yield db
    finally:
        db.close() 


def overide_get_current_user():
    return {'username': 'firsttest', 'id': 7, 'role': 'admin'}


@pytest.fixture
def test_todo():
    todo = Todos(
        title ="running",
        description="for race",
        priority= 7,
        complete= True,
        id= 1,
        owner_id= 7
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text('Delete from todos;'))
        connection.commit()




@pytest.fixture
def test_user():
        user = Users(
        username= "firsttest",
        email= "firsttest@gmail.com",
        last_name= "test",
        is_active= True,
        phone_number= "12121212",
        id =7,
        first_name= "first",
        hashed_password= bcrypt_context.hash("firsttest"),
        role= "admin"
    )

        db = TestingSessionLocal()
        db.add(user)
        db.commit()
        yield user
        with engine.connect() as connection:
                connection.execute(text('Delete from users;'))
                connection.commit()
