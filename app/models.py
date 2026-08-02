"""
Core data models.

Employee   -> a worker whose real-time status is derived from their tasks
Task       -> unit of work with a due date and lifecycle status
"""
import enum
from datetime import datetime

from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey, Enum, Text, Boolean
)
from sqlalchemy.orm import relationship

from app.database import Base


class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    OVERDUE = "overdue"


class EmployeeStatus(str, enum.Enum):
    IDLE = "idle"
    WORKING = "working"
    OVERDUE = "overdue"


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    department = Column(String(100), default="General")
    status = Column(Enum(EmployeeStatus), default=EmployeeStatus.IDLE)
    created_at = Column(DateTime, default=datetime.utcnow)

    tasks = relationship("Task", back_populates="employee", cascade="all, delete-orphan")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, default="")
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING)
    priority = Column(String(20), default="medium")
    due_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    reminder_sent = Column(Boolean, default=False)

    employee = relationship("Employee", back_populates="tasks")