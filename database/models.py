from sqlalchemy import Column, Integer, String, Boolean
from database.database import Base

class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, index=False, nullable=True )
    completed = Column(Boolean, default=False)