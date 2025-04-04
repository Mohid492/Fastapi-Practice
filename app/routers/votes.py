from http.client import HTTPException
from typing import Optional
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
import time
from .. import models
from ..database import engine,get_db
from .. import  schemas,utils,oauth2

router=APIRouter(prefix="/votes",tags=["Votes"])

@router.post("/",status_code=status.HTTP_201_CREATED)
async def vote(vote: schemas.Vote,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):

    post=db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with id {vote.post_id} does not exist")
    vote_query=db.query(models.Vote).filter(models.Vote.post_id==vote.post_id,
                                      models.Vote.user_id==current_user.id)
    found_vote=vote_query.first()
    if vote.dir==1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="You have already voted the post")
        new_vote=models.Vote(post_id=vote.post_id,user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"successfully voted"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"successfully unvoted"}

