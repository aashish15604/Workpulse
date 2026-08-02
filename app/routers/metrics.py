from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import models

router = APIRouter(prefix="/api/metrics", tags=["metrics"])


@router.get("/overview")
def overview(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).all()
    total = len(tasks)
    completed = sum(1 for t in tasks if t.status == models.TaskStatus.COMPLETED)
    in_progress = sum(1 for t in tasks if t.status == models.TaskStatus.IN_PROGRESS)
    pending = sum(1 for t in tasks if t.status == models.TaskStatus.PENDING)
    overdue = sum(1 for t in tasks if t.status == models.TaskStatus.OVERDUE)
    rate = round((completed / total) * 100, 1) if total else 0.0

    return {
        "total_tasks": total,
        "completed": completed,
        "in_progress": in_progress,
        "pending": pending,
        "overdue": overdue,
        "completion_rate": rate,
    }


@router.get("/employees")
def employee_metrics(db: Session = Depends(get_db)):
    employees = db.query(models.Employee).all()
    results = []
    for emp in employees:
        assigned = emp.tasks
        completed_tasks = [t for t in assigned if t.status == models.TaskStatus.COMPLETED]
        overdue_count = sum(1 for t in assigned if t.status == models.TaskStatus.OVERDUE)

        results.append({
            "employee_id": emp.id,
            "name": emp.name,
            "status": emp.status,
            "total_assigned": len(assigned),
            "completed": len(completed_tasks),
            "overdue": overdue_count,
            "completion_rate": round((len(completed_tasks) / len(assigned)) * 100, 1) if assigned else 0.0,
        })
    return results