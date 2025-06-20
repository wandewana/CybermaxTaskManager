from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Schema for creating a task
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None

# Schema for updating a task
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    is_completed: Optional[bool] = None

# Base schema for a task, used for responses
class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    is_completed: bool
    owner_id: int

    class Config:
        orm_mode = True
