from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.models import TaskStatus, EmployeeStatus


# ---------- Employee ----------
class EmployeeCreate(BaseModel):
    name: str
    email: str
    department: str = "General"


class EmployeeOut(BaseModel):
    id: int
    name: str
    email: str
    department: str
    status: EmployeeStatus

    class Config:
        from_attributes = True


# ---------- Task ----------
class TaskCreate(BaseModel):
    title: str
    description: str = ""
    employee_id: int
    priority: str = "medium"
    due_date: datetime


class TaskUpdate(BaseModel):
    status: Optional[TaskStatus] = None
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None


class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    employee_id: int
    status: TaskStatus
    priority: str
    due_date: datetime
    created_at: datetime
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True