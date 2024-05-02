from sqlalchemy.orm import Session

from . import models, schemas

from passlib.context import CryptContext
brcypt_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")


#UTILITS
def create_token(user: schemas.TokenCreate) -> schemas.Token:
    token = schemas.Token()
    return token



def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = brcypt_context.hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user 


def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).offset(skip).limit(limit).all()

def get_token(db: Session, token: schemas.Token, user: schemas.TokenCreate):
    token = create_token(user)
    return token


def create_user_task(db: Session, task: schemas.TaskCreate, user_id: int):
    db_task = models.Task(**task.dict(), owner_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return user
    return None

def delete_task(db: Session, task_id: int):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
        return task
    return None

def update_task(db: Session, task_id: int, task_data: schemas.TaskUpdate):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task:
        for key, value in task_data.dict().items():
            setattr(task, key, value)
        db.commit()
        db.refresh(task)
        return task
    return None

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        for attr, value in user_update.dict().items():
            setattr(db_user, attr, value)
        db.commit()
        db.refresh(db_user)
        return db_user
    return None