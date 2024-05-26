import logging
import sys
from contextlib import asynccontextmanager



# Comando para executar o arquivo .sh

import asyncpg
import uvicorn
from app.config import settings
from app.databaseTeste import sessionmanager, get_db_session, AsyncSession
from fastapi import Depends, FastAPI, HTTPException
from . import crud,  schemas



class db_config():
    def __init__(self) -> None:
        self.async_pool = None

    async def init_db(self):
         
         self.async_pool = await self.get_db_pool()
        

    async def get_db_pool(self):
        pool = await asyncpg.create_pool(
            user='username',
            password='password',
            database='postgres_async',
            host='postgres_async',
            port='5432'
        )
        return pool

db = db_config()

async def get_pool_session():
    if db.async_pool == None:
        await db.init_db()
    return db.async_pool


logging.basicConfig(stream=sys.stdout, level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """
    yield
    if sessionmanager._engine is not None:
        # Close the DB connection
        await sessionmanager.close()


app = FastAPI(lifespan=lifespan, title=settings.project_name, docs_url="/api/docs")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/users/", response_model=schemas.User)
async def create_user(
    user: schemas.UserCreate, db: AsyncSession = Depends(get_db_session)):
    db_user = await crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: asyncpg.Pool = Depends(get_pool_session)):
    users = await crud.get_users(db, skip=skip, limit=limit)
    if users is None:
        raise HTTPException(status_code=404, detail="Users not found")
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db_session)):
    db_user = await crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/tasks/", response_model=schemas.Task)
async def create_task_for_user(
    user_id: int, task: schemas.TaskBase, db: AsyncSession = Depends(get_db_session)
):
    return await crud.create_user_task(db=db, task=task, user_id=user_id)


@app.get("/tasks/", response_model=list[schemas.Task])
async def read_tasks(skip: int = 0, limit: int = 100, db: asyncpg.Pool = Depends(get_pool_session)):
    tasks = await crud.get_tasks(db, skip=skip, limit=limit)
    return tasks


@app.delete("/users/{user_id}", response_model=schemas.User)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db_session)):
    db_user = await crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return await crud.delete_user(db=db, user_id=user_id)

@app.delete("/tasks/{task_id}", response_model=schemas.TaskDelete)
async def delete_task(task_id: int, db: asyncpg.Pool = Depends(get_pool_session)):
    return await crud.delete_task(pool=db, task_id=task_id)


@app.get("/users/auth/{email}/{password}", response_model=schemas.Token)
async def get_token_user(
    email: str, password:str, db: AsyncSession = Depends(get_db_session)
    ):
    return await crud.create_token(db=db, email=email, password=password)

@app.put("/users/{user_id}", response_model=schemas.User)
async def update_user(
    user_id: int, user_update: schemas.UserUpdate, db: AsyncSession = Depends(get_db_session)
    ):
    db_user = await crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return await crud.update_user(db=db, user_id=user_id, user_update=user_update)


@app.put("/tasks/{task_id}", response_model=dict)
async def update_task(task_id: int, task_update: schemas.TaskUpdate, db: asyncpg.Pool = Depends(get_pool_session)):
    return await crud.update_task(db=db, task_id=task_id, task_data=task_update)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)