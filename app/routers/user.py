from http.client import HTTPException
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from .. import models
from ..database import engine,get_db
from .. import  schemas,utils


router = APIRouter(prefix="/users",tags=["Users"])
# CURD for users

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate,db: Session = Depends(get_db)):

    hashed_password=utils.hash(user.password) #Hash the user's password and replace the plain text password with the hashed version.
    user.password=hashed_password
    new_user=models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",response_model=schemas.UserResponse)
async def get_user(id: int,db: Session = Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} does not exist"
        )
    return user


