from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post,user,auth,votes
from fastapi.middleware.cors import CORSMiddleware

#models.Base.metadata.create_all(bind=engine)
app=FastAPI()

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(votes.router)
@app.get("/")
async def root():
    return {"message":"Starting Fastapi"}

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "https://www.google.com"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
