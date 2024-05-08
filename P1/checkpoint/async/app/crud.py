from . import models, schemas

from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
bcrypt_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")


#UTILITS
def create_token(user: schemas.TokenCreate) -> schemas.Token:
    token = schemas.Token()
    return token



async def get_user(db: AsyncSession, user_id: int):
    user = (await db.scalars(select(models.User).where(models.User.id == user_id))).first()
    return user

async def get_task(db: AsyncSession, task_id: int):
    return (await db.scalars(select(models.Task).where(models.Task.id == task_id))).first() 

async def get_user_by_email(db: AsyncSession, email: str):
    return (await db.scalars(select(models.User).where(models.User.email == email))).first()


import asyncpg

async def get_users(pool: asyncpg.Pool, skip: int = 0, limit: int = 100):
    try:
        async with pool.acquire() as connection:
            # Executa a consulta SQL diretamente
            query = f"SELECT * FROM users OFFSET {skip} LIMIT {limit}"
            rows = await connection.fetch(query)

            # Transforma as linhas em dicionários
            users = [dict(row) for row in rows]
            return users
    except Exception as e:
        print(f"Erro ao obter usuários: {e}")
        return None
    
    

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    hashed_password = bcrypt_context.hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password, is_active=True)
    db.add(db_user)
    await db.commit()  # Aguardar o commit
    await db.refresh(db_user)  # Aguardar o refresh
    return db_user



async def get_tasks(pool: asyncpg.Pool, skip: int = 0, limit: int = 100):
    try:
        async with pool.acquire() as connection:
            # Executa a consulta SQL diretamente
            query = f"SELECT * FROM tasks OFFSET {skip} LIMIT {limit}"
            rows = await connection.fetch(query)

            # Transforma as linhas em dicionários
            users = [dict(row) for row in rows]
            return users
    except Exception as e:
        print(f"Erro ao obter usuários: {e}")
        return None
    

async def get_token(db: AsyncSession, token: schemas.Token, user: schemas.TokenCreate):
    token = create_token(user)
    return token


async def create_user_task(db: AsyncSession, task: schemas.TaskCreate, user_id: int):
    db_task = models.Task(title=task.title, description=task.description, owner_id=user_id)
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task


async def delete_user(db: AsyncSession, user_id: int):
    user = (await db.scalars(select(models.User).where(models.User.id == user_id))).first()
    if user:
        await db.delete(user)
        await db.commit()
        return user
    return None

async def delete_task(db: AsyncSession, task_id: int):
    task = (await db.scalars(select(models.Task).where(models.Task.id == task_id))).first() 
    if task:
        db.delete(task)
        db.commit()
        return task
    return None

async def update_task(db: AsyncSession, task_id: int, task_data: schemas.TaskUpdate):
    task = (await db.scalars(select(models.Task).where(models.Task.id == task_id))).first() 
    if task:
        for key, value in task_data.dict().items():
            setattr(task, key, value)
        db.commit()
        db.refresh(task)
        return task
    return None

async def update_user(db: AsyncSession, user_id: int, user_update: schemas.UserUpdate):
    db_user = (await db.scalars(select(models.User).where(models.User.id == user_id))).first()
    if db_user:
        for attr, value in user_update.dict().items():
            setattr(db_user, attr, value)
        db.commit()
        db.refresh(db_user)
        return db_user
    return None