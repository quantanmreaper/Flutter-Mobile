from fastapi import FastAPI, Depends , HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database.database import engine, get_db, Base
from database.models import models

Base.metadata.create_all(bind=engine)

app = FastAPI()

class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False
    
class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    completed: bool

#get root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Task Manager API"}

#seeing if the API is running
@app.get("/health")
def read_health():
    return {"status": "ok"}

#retrieving all tasks
@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    return db.query(models.TaskModel).all()

#fetching only completed tasks
@app.get("/tasks/completed")
def get_completed_tasks(db: Session = Depends(get_db)):
    return db.query(models.TaskModel).filter(
        models.TaskModel.completed == True
    ).all()

@app.get("/tasks/{task_id}")
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.TaskModel).filter(
        models.TaskModel.id == task_id   
    ).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    if not task.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    new_task = models.TaskModel(
        title = task.title,
        description = task.description,
        completed = task.completed,
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, updated: TaskCreate, db: Session = Depends(get_db)):
    task = db.query(models.TaskModel).filter(
        models.TaskModel.id == task_id
    ).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    task.title = updated.title
    task.completed = updated.completed
    task.description = updated.description
    db.commit()
    db.refresh(task)
    return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.TaskModel).filter(
        models.TaskModel.id == task_id
    ).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": f"Task {task_id} deleted successfully"}