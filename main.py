from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, ConfigDict, Field, field_validator
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text

import models
from database import engine, get_db
# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Python Task Management API",
    description="A beginner-friendly REST API with SQLite",
    version="2.0.0"
)


# Request model for creating tasks

from pydantic import BaseModel, ConfigDict, Field, field_validator


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(default="", max_length=500)
    completed: bool = False

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        value = value.strip()

        if not value:
            raise ValueError("Task title cannot be empty or contain only spaces")

        return value


# Request model for updating tasks

class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    completed: bool | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        if value is None:
            return value

        value = value.strip()

        if not value:
            raise ValueError("Task title cannot be empty or contain only spaces")

        return value


# Response model
class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    completed: bool

    model_config = ConfigDict(from_attributes=True)


@app.get("/")
def home():
    return {
        "message": "Welcome to the Task Management API",
        "status": "running"
    }


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "healthy"}

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=503,
            detail="Database unavailable"
        )

# Create a task
@app.post("/tasks", status_code=201, response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    try:
        new_task = models.Task(
            title=task.title,
            description=task.description,
            completed=task.completed
        )

        db.add(new_task)
        db.commit()
        db.refresh(new_task)

        return new_task

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while creating task"
        )

# Get all tasks
@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).all()


# Get one task
@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


# Update a task
# Update a task
@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    updated_task: TaskUpdate,
    db: Session = Depends(get_db)
):
    task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    changes = updated_task.model_dump(exclude_unset=True)

    if not changes:
        raise HTTPException(
            status_code=400,
            detail="No update fields provided"
        )

    if any(value is None for value in changes.values()):
        raise HTTPException(
            status_code=422,
            detail="Task fields cannot be null"
        )

    try:
        for key, value in changes.items():
            setattr(task, key, value)

        db.commit()
        db.refresh(task)

        return task

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while updating task"
        )
    for key, value in changes.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)

    return task


# Delete a task

# Delete a task
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(
        models.Task.id == task_id
    ).first()

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    deleted_task = {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed
    }

    try:
        db.delete(task)
        db.commit()

        return {
            "message": "Task deleted successfully",
            "task": deleted_task
        }

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error occurred while deleting task"
        )
