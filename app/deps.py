"""
FastAPI dependency for reading the logged-in employee from the session cookie.
"""
from fastapi import Request, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.security import SESSION_COOKIE_NAME, read_session_token


def get_current_employee(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get(SESSION_COOKIE_NAME)
    if not token:
        return None
    employee_id = read_session_token(token)
    if not employee_id:
        return None
    return db.get(models.Employee, employee_id)