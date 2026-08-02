"""
Email notifications — sends an alert when a task goes overdue.
Uses Gmail SMTP with an app password (see .env file).
"""
import logging
import os
import smtplib
from email.mime.text import MIMEText

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("workpulse.notifications")

GMAIL_ADDRESS = os.environ.get("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")


def send_overdue_email(to_email: str, employee_name: str, task_title: str, due_date):
    if not GMAIL_ADDRESS or not GMAIL_APP_PASSWORD:
        logger.warning("Email credentials not configured, skipping notification.")
        return

    subject = f"Task Overdue: {task_title}"
    body = (
        f"Hi {employee_name},\n\n"
        f"Your task \"{task_title}\" was due on {due_date.strftime('%d %b %Y, %I:%M %p')} "
        f"and is now marked as overdue.\n\n"
        f"Please update its status in WorkPulse as soon as possible.\n\n"
        f"— WorkPulse"
    )

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = to_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_ADDRESS, to_email, msg.as_string())
        logger.info(f"Overdue email sent to {to_email} for task '{task_title}'")
    except Exception:
        logger.exception(f"Failed to send overdue email to {to_email}")

def send_reminder_email(to_email: str, employee_name: str, task_title: str, due_date):
    if not GMAIL_ADDRESS or not GMAIL_APP_PASSWORD:
        logger.warning("Email credentials not configured, skipping notification.")
        return

    subject = f"Reminder: {task_title} is due soon"
    body = (
        f"Hi {employee_name},\n\n"
        f"Just a reminder that your task \"{task_title}\" is due on "
        f"{due_date.strftime('%d %b %Y, %I:%M %p')}.\n\n"
        f"Please make sure to complete it on time.\n\n"
        f"— WorkPulse"
    )

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = to_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_ADDRESS, to_email, msg.as_string())
        logger.info(f"Reminder email sent to {to_email} for task '{task_title}'")
    except Exception:
        logger.exception(f"Failed to send reminder email to {to_email}")