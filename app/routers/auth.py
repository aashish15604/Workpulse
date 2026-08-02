from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app import models
from app.security import (
    hash_password, verify_password, create_session_token,
    SESSION_COOKIE_NAME, SESSION_MAX_AGE_SECONDS,
)

router = APIRouter(tags=["auth"])
templates = Jinja2Templates(directory="app/templates")


@router.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse(request=request, name="register.html", context={"error": None})


@router.post("/register")
def register_submit(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    department: str = Form("General"),
    password: str = Form(...),
    confirm_password: str = Form(...),
    db: Session = Depends(get_db),
):
    error = None
    if password != confirm_password:
        error = "Passwords do not match."
    elif len(password) < 6:
        error = "Password must be at least 6 characters."
    elif db.query(models.Employee).filter_by(email=email).first():
        error = "An account with this email already exists."

    if error:
        return templates.TemplateResponse(
            request=request, name="register.html",
            context={"error": error, "name": name, "email": email, "department": department},
        )

    employee = models.Employee(
        name=name, email=email, department=department,
        hashed_password=hash_password(password),
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)

    return RedirectResponse(url="/login", status_code=303)


@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html", context={"error": None})


@router.post("/login")
def login_submit(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    employee = db.query(models.Employee).filter_by(email=email).first()
    if not employee or not verify_password(password, employee.hashed_password):
        return templates.TemplateResponse(
            request=request, name="login.html",
            context={"error": "Invalid email or password.", "email": email},
        )

    response = RedirectResponse(url="/", status_code=303)
    token = create_session_token(employee.id)
    response.set_cookie(SESSION_COOKIE_NAME, token, max_age=SESSION_MAX_AGE_SECONDS, httponly=True, samesite="lax")
    return response


@router.get("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie(SESSION_COOKIE_NAME)
    return response