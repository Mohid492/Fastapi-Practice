from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from .. import  database,schemas,models,utils,oauth2
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=schemas.Token)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    access_token_expires = timedelta(minutes=oauth2.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = oauth2.create_access_token(data={"user_id": user.id}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}
