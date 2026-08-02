# WorkPulse

An automated task scheduling and monitoring system with real-time employee status tracking, a live metrics dashboard, and proactive email notifications.

Built to eliminate manual status tracking - a background scheduler continuously monitors tasks, automatically flags overdue work, updates employee status, and emails the assigned employee both a reminder before the deadline and an alert if it's missed.

## Features

- User registration and login with hashed passwords and session cookies
- Task management - create tasks, assign to employees, set priority and due date
- Automated background scheduler that flags overdue tasks and updates employee status automatically
- Email notifications - a reminder before the deadline, and an overdue alert if missed
- Live dashboard with overview cards and employee status table
- Interactive task list - create, start, and complete tasks without touching the database directly

## Tech Stack

- FastAPI (API framework)
- SQLAlchemy (ORM)
- APScheduler (background scheduling)
- Passlib + itsdangerous (authentication)
- Gmail SMTP (email notifications)
- SQLite (database)
- Jinja2 + vanilla JavaScript (frontend)

## Getting Started

1. Clone the repository
2. Create a virtual environment: python -m venv venv
3. Activate it: venv\Scripts\Activate.ps1
4. Install dependencies: pip install -r requirements.txt
5. Create a .env file with GMAIL_ADDRESS and GMAIL_APP_PASSWORD (optional, for email notifications)
6. Run the server: uvicorn app.main:app --reload
7. Open http://localhost:8000

## How the Automation Works

A background job runs on a recurring interval and:
1. Scans all non-completed tasks
2. Flags any task past its due date as overdue, and emails the assigned employee
3. Sends a reminder email if a task is nearing its due date and no reminder has been sent yet
4. Recomputes each employee's live status (idle, working, or overdue) based on their current tasks

No status is ever set manually - it is always derived automatically from real task data.