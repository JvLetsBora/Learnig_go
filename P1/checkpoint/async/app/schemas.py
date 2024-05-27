from pydantic import BaseModel
from typing import List

class TaskBase(BaseModel):
    title: str
    description: str


class TaskCreate(TaskBase):
    pass

class TaskDelete(BaseModel):
    msg : str

class UserDelete(BaseModel):
    msg : str

class UserUpdate(BaseModel):
    email: str
    password: str


class TaskUpdate(BaseModel):
    title: str
    description: str

class Task(TaskBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int = None
    is_active: bool = False
    tasks: List[Task] = []

    class Config:
        orm_mode = True



class Token(BaseModel):
    access_token: int

class TokenCreate(BaseModel):
    id: int
    password: str