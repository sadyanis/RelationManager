from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World thefka mlih"}

