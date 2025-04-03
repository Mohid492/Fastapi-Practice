from typing import Optional

from pydantic import BaseModel, Field, EmailStr, conint
from datetime import datetime, date

class Post(BaseModel):
    title:str
    content:str
    published:bool=True
    created_at: date = Field(default_factory=date.today)

class UpdatePost(BaseModel):
    title:str
    content:str
    published:bool
    created_at: date

class UserResponse(BaseModel):
    id:int
    email:EmailStr

class PostResponse(BaseModel):
    id:int
    owner_id: int
    title:str
    content:str
    published:bool
    owner:UserResponse

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email:EmailStr
    password:str


    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email:EmailStr
    password:str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id:int
    dir:conint(le=1)

class PostOut(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True