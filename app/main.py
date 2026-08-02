"""
WorkPulse — Automated Task Scheduling & Metrics Dashboard
"""
import logging

from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.database import Base, engine, get_db
from app.routers import employees, tasks, metrics, auth
from app import models
from sqlalchemy.orm import Session
from app.deps import get_current_employee
from fastapi.responses import RedirectResponse
from app.scheduler import start_scheduler

logging.basicConfig(level=logging.INFO)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="WorkPulse",
    description="Automated task scheduling system with a centralized metrics dashboard.",
    version="1.0.0",
)

app.include_router(employees.router)
app.include_router(tasks.router)
app.include_router(metrics.router)
app.include_router(auth.router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/")
def dashboard(request: Request, employee=Depends(get_current_employee)):
    if not employee:
        return RedirectResponse(url="/login", status_code=303)
    return templates.TemplateResponse(request=request, name="dashboard.html", context={"employee": employee})
@app.get("/tasks")
def tasks_page(request: Request, employee=Depends(get_current_employee), db: Session = Depends(get_db)):
    if not employee:
        return RedirectResponse(url="/login", status_code=303)
    employees = db.query(models.Employee).order_by(models.Employee.name).all()
    return templates.TemplateResponse(
        request=request, name="tasks.html",
        context={"employee": employee, "employees": employees},
    )

_scheduler = None


@app.on_event("startup")
def on_startup():
    global _scheduler
    _scheduler = start_scheduler()


@app.on_event("shutdown")
def on_shutdown():
    if _scheduler:
        _scheduler.shutdown()


@app.get("/health")
def health():
    return {"status": "ok"}