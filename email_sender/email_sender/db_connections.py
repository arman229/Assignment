from contextlib import asynccontextmanager 
from email_sender import settings
from sqlmodel import Field, Session, SQLModel, create_engine, select, Sequence
from fastapi import FastAPI, Depends
from typing import AsyncGenerator
from typing import Annotated

connection_string = str(settings.DATABASE_URL).replace("postgresql", "postgresql+psycopg")
engine = create_engine(    connection_string, connect_args={}, pool_recycle=300)
def create_db_and_tables()->None:
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
        
        
@asynccontextmanager
async def lifespan(app: FastAPI)-> AsyncGenerator[None, None]:
    print("Creating tables..") 
    create_db_and_tables()
    yield


DB_SESSION = Annotated[Session, Depends(get_session)]


        