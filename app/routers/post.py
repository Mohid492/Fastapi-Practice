from http.client import HTTPException
from typing import Optional
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
import time
from .. import models
from ..database import engine,get_db
from .. import  schemas,utils,oauth2

router=APIRouter(prefix="/posts",tags=["Posts"])

@router.get("/",response_model=list[schemas.PostOut])
async def get_posts(db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user),
                    limit:int=10,skip:int=0,search:Optional[str]=""):
    # posts = db.query(models.Post).filter(models.Post.title.icontains(search)).limit(limit).offset(skip).all() #/post?limit={}&skip={}
    posts = (db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id)
               .filter(models.Post.title.icontains(search)).limit(limit).offset(skip).all())

    return posts

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
async def create_posts(post: schemas.Post,db: Session = Depends(get_db),
                       current_user:int=Depends(oauth2.get_current_user)):
    new_post=models.Post(owner_id=current_user.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}",response_model=schemas.PostOut)
async def get_specific_post(id: int,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    #post=db.query(models.Post).filter(models.Post.id==id).first()
    post = (db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
            .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
            .group_by(models.Post.id)
            .filter(models.Post.id == id)
            .first())
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")
    # if post.owner_id!=current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail=f"Not authorized to view this post")

    return post



@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT,)
async def delete_post(id:int,db: Session = Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    post_to_delete=db.query(models.Post).filter(models.Post.id==id).first()
    if post_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")

    if post_to_delete.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to delete this post")

    db.delete(post_to_delete)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.PostResponse)
async def update_post(id: int, post_data: schemas.UpdatePost, db: Session = Depends(get_db),
                      current_user:int=Depends(oauth2.get_current_user)):
    query = db.query(models.Post).filter(models.Post.id == id)
    existing_post = query.first()
    if existing_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )

    if existing_post.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to update this post")

    query.update(post_data.model_dump(), synchronize_session=False)
    db.commit()
    db.refresh(existing_post)

    return {"data": existing_post}
