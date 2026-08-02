from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get("/", response_model=list[schemas.TaskOut])
def list_tasks(
    employee_id: int | None = None,
    status: models.TaskStatus | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(models.Task)
    if employee_id is not None:
        query = query.filter(models.Task.employee_id == employee_id)
    if status is not None:
        query = query.filter(models.Task.status == status)
    return query.order_by(models.Task.due_date).all()


@router.post("/", response_model=schemas.TaskOut, status_code=201)
def create_task(payload: schemas.TaskCreate, db: Session = Depends(get_db)):
    if not db.get(models.Employee, payload.employee_id):
        raise HTTPException(404, "Employee not found")
    task = models.Task(**payload.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.patch("/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int, payload: schemas.TaskUpdate, db: Session = Depends(get_db)):
    task = db.get(models.Task, task_id)
    if not task:
        raise HTTPException(404, "Task not found")

    data = payload.model_dump(exclude_unset=True)
    if data.get("status") == models.TaskStatus.COMPLETED and task.completed_at is None:
        task.completed_at = datetime.utcnow()

    for field, value in data.items():
        setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task