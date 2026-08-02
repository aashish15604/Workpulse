"""
Background scheduling engine.

Runs on a recurring interval, scans all tasks, flips anything past its
due date into OVERDUE, and recomputes each employee's real-time status
(idle / working / overdue) purely from their current task set.
"""
import logging
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler

from app.database import SessionLocal
from app.models import Task, Employee, TaskStatus, EmployeeStatus
from app.notifications import send_overdue_email, send_reminder_email
from datetime import timedelta

logger = logging.getLogger("workpulse.scheduler")

SWEEP_INTERVAL_SECONDS = 60
REMINDER_WINDOW_MINUTES = 3


def sweep_task_statuses():
    db = SessionLocal()
    try:
        now = datetime.now()

        active_tasks = db.query(Task).filter(Task.status != TaskStatus.COMPLETED).all()
        for task in active_tasks:
            if task.due_date < now and task.status != TaskStatus.OVERDUE:
                task.status = TaskStatus.OVERDUE
                logger.info(f"Task {task.id} '{task.title}' marked OVERDUE")
                if task.employee:
                    send_overdue_email(
                        to_email=task.employee.email,
                        employee_name=task.employee.name,
                        task_title=task.title,
                        due_date=task.due_date,
                    )
            elif not task.reminder_sent and task.status != TaskStatus.OVERDUE:
                reminder_time = task.due_date - timedelta(minutes=REMINDER_WINDOW_MINUTES)
                if now >= reminder_time:
                    task.reminder_sent = True
                    logger.info(f"Task {task.id} '{task.title}' reminder triggered")
                    if task.employee:
                        send_reminder_email(
                            to_email=task.employee.email,
                            employee_name=task.employee.name,
                            task_title=task.title,
                            due_date=task.due_date,
                        )

        employees = db.query(Employee).all()
        for emp in employees:
            emp_tasks = [t for t in emp.tasks if t.status != TaskStatus.COMPLETED]
            if any(t.status == TaskStatus.OVERDUE for t in emp_tasks):
                emp.status = EmployeeStatus.OVERDUE
            elif any(t.status == TaskStatus.IN_PROGRESS for t in emp_tasks):
                emp.status = EmployeeStatus.WORKING
            else:
                emp.status = EmployeeStatus.IDLE

        db.commit()
    except Exception:
        logger.exception("Sweep failed")
        db.rollback()
    finally:
        db.close()


def start_scheduler() -> BackgroundScheduler:
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        sweep_task_statuses,
        "interval",
        seconds=SWEEP_INTERVAL_SECONDS,
        id="status_sweep",
        replace_existing=True,
    )
    scheduler.start()
    logger.info(f"Scheduler started (sweep every {SWEEP_INTERVAL_SECONDS}s)")
    return scheduler