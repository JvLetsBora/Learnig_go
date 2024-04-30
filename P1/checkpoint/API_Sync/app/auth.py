from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from starlette import status
from database import SessionLocal
from models import User
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

SECRET_KEY = "09d25e094faa6camuricola6b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Token(BaseModel):
    access_token: str
    token_type: str

class CreateUserRequest(BaseModel):
    email: str
    password: str

class TokenData(BaseModel):
    username: str 

brcypt_context = CryptContext(schemes=["brcypt"], deprecated="auto")
auth2bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependence = Annotated[Session, Depends(get_db)]

