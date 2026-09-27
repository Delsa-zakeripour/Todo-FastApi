from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# DATABASE_URL='postgresql://delsa@localhost/TodoAppliicationDatabase'
# engine = create_engine(DATABASE_URL)

SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})



sessionLocal = sessionmaker(autocommit= False, autoflush=False, bind=engine)

Base = declarative_base()
