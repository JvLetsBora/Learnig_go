import logging
import sys
from contextlib import asynccontextmanager

import uvicorn
from app.config import settings
from app.databaseTeste import sessionmanager, get_db_session, AsyncSession
from fastapi import Depends, FastAPI, HTTPException
from . import crud,  schemas



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
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db_session)):
    users = await crud.get_users(db, skip=skip, limit=limit)
    if users is None:
        raise HTTPException(status_code=404, detail="User not found")
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: AsyncSession = Depends(get_db_session)):
    db_user = await crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/tasks/", response_model=schemas.Task)
async def create_task_for_user(
    user_id: int, task: schemas.TaskCreate, db: AsyncSession = Depends(get_db_session)
):
    return crud.create_user_task(db=db, task=task, user_id=user_id)


@app.get("/tasks/", response_model=list[schemas.Task])
async def read_tasks(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db_session)):
    tasks = await crud.get_tasks(db, skip=skip, limit=limit)
    return tasks


@app.delete("/users/{user_id}", response_model=schemas.User)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db_session)):
    db_user = await crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.delete_user(db=db, user_id=user_id)

@app.delete("/tasks/{task_id}", response_model=schemas.Task)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db_session)):
    db_task = await crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return crud.delete_task(db=db, task_id=task_id)


@app.put("/users/{user_id}", response_model=schemas.User)
async def update_user(user_id: int, user_update: schemas.UserUpdate, db: AsyncSession = Depends(get_db_session)):
    db_user = await crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.update_user(db=db, user_id=user_id, user_update=user_update)


@app.put("/tasks/{task_id}", response_model=schemas.Task)
async def update_task(task_id: int, task_update: schemas.TaskUpdate, db: AsyncSession = Depends(get_db_session)):
    db_task = await crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return crud.update_task(db=db, task_id=task_id, task_update=task_update)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)