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

