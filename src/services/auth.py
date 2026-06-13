# filepath: src/services/auth.py

"""The ONLY module that hashes passwords or mints/verifies JWTs."""

import enum
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from email_validator import EmailNotValidError, validate_email
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from config import settings
from db.models import User

ALGORITHM = "HS256"


class TokenPurpose(str, enum.Enum):
    ACCESS = "access"
    REFRESH = "refresh"
    EMAIL_VERIFY = "email_verify"
    PW_RESET = "pw_reset"


# --- passwords ---------------------------------------------------------------


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except ValueError:
        return False


# --- tokens ------------------------------------------------------------------


def _mint(sub: str, purpose: TokenPurpose, lifetime: timedelta) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": sub,
        "purpose": purpose.value,
        "iat": now,
        "exp": now + lifetime,
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)


def create_access_token(user_id: int) -> str:
    return _mint(
        str(user_id), TokenPurpose.ACCESS, timedelta(minutes=settings.ACCESS_TOKEN_MINUTES)
    )


def create_refresh_token(user_id: int) -> str:
    return _mint(str(user_id), TokenPurpose.REFRESH, timedelta(days=settings.REFRESH_TOKEN_DAYS))


def create_email_verify_token(user_id: int) -> str:
    return _mint(
        str(user_id), TokenPurpose.EMAIL_VERIFY, timedelta(hours=settings.EMAIL_TOKEN_HOURS)
    )


def create_pw_reset_token(user_id: int) -> str:
    return _mint(str(user_id), TokenPurpose.PW_RESET, timedelta(hours=settings.EMAIL_TOKEN_HOURS))


def decode_token(token: str, expected_purpose: TokenPurpose) -> dict:
    """Decode and validate a token, enforcing its purpose claim.

    A token minted for one purpose can never be accepted for another —
    an email-verify link must not authenticate API requests.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token expired") from None
    except jwt.InvalidTokenError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token") from None

    if payload.get("purpose") != expected_purpose.value:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token")
    if "sub" not in payload:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token")
    return payload


def token_pair(user_id: int) -> dict:
    return {
        "access_token": create_access_token(user_id),
        "refresh_token": create_refresh_token(user_id),
        "token_type": "bearer",
    }


# --- account operations -------------------------------------------------------


def normalize_email(email: str) -> str:
    """Validate and fully lowercase. email_validator lowercases only the domain;
    real providers treat the local part case-insensitively too, and a
    case-sensitive local part lets one mailbox register twice."""
    try:
        return validate_email(email, check_deliverability=False).normalized.lower()
    except EmailNotValidError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e)) from None


def register_user(db: Session, email: str, password: str) -> User:
    email = normalize_email(email)
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Email already registered")
    user = User(email=email, password_hash=hash_password(password))
    db.add(user)
    db.flush()  # assign user.id
    return user


def authenticate(db: Session, email: str, password: str) -> User:
    email = normalize_email(email)
    user = db.query(User).filter(User.email == email).first()
    # Same error for unknown user, wrong password, AND telegram-only accounts
    # (password_hash is None) — anything more specific enumerates accounts.
    if (
        user is None
        or user.password_hash is None
        or not verify_password(password, user.password_hash)
    ):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid email or password")
    return user


def bridge_telegram_user(
    db: Session, telegram_id: int, telegram_handle: str | None
) -> tuple[User, bool]:
    """Create-or-fetch the account behind a Telegram identity.

    Returns (user, created). Trust is the caller's responsibility — the
    router verifies the bridge secret before calling this.
    """
    tg_id = str(telegram_id)
    user = db.query(User).filter(User.telegram_id == tg_id).first()
    created = False
    if user is None:
        user = User(telegram_id=tg_id, telegram_handle=telegram_handle)
        db.add(user)
        db.flush()
        created = True
    elif telegram_handle and user.telegram_handle != telegram_handle:
        user.telegram_handle = telegram_handle  # handle drift
    return user, created


def get_user_from_token(db: Session, token: str, purpose: TokenPurpose) -> User:
    payload = decode_token(token, purpose)
    user = db.get(User, int(payload["sub"]))
    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token")
    return user
