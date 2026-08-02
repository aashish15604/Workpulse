"""
Auth utilities: password hashing + signed session tokens (stored in a
browser cookie).
"""
import os

from passlib.context import CryptContext
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

SECRET_KEY = os.environ.get("WORKPULSE_SECRET_KEY", "dev-secret-change-in-production")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
serializer = URLSafeTimedSerializer(SECRET_KEY, salt="workpulse-session")

SESSION_COOKIE_NAME = "wp_session"
SESSION_MAX_AGE_SECONDS = 7 * 24 * 3600  # 7 days


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_session_token(employee_id: int) -> str:
    return serializer.dumps({"employee_id": employee_id})


def read_session_token(token: str):
    try:
        data = serializer.loads(token, max_age=SESSION_MAX_AGE_SECONDS)
        return data.get("employee_id")
    except (BadSignature, SignatureExpired):
        return None