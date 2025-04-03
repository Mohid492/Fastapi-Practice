from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlmodel import Field, Session, SQLModel, create_engine, select
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/post_db"
engine=create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base=declarative_base()

#Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# The get_db function is a dependency used in FastAPI to provide a database
# session for each request. It ensures that the session
# is properly opened and closed, preventing potential database connection leaks.