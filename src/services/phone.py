# filepath: src/services/phone.py

"""Phone verification flow: our own OTP, any SMS backend.

We generate and check the codes ourselves (hash at rest, TTL, attempt cap,
resend cooldown) so the SMS provider stays a dumb pipe — swapping Twilio
for anything else never touches this logic.
"""

import hashlib
import re
import secrets
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from config import settings
from db.base import utcnow
from db.models import SmsVerification, User
from services.sms import get_sms_backend

_PHONE_RE = re.compile(r"^\+[0-9]{8,15}$")

CODE_MESSAGE = "Your Crowdjump verification code: {code}"


def normalize_phone(raw: str) -> str:
    """Light E.164 normalization: strip separators, require +<8..15 digits>."""
    cleaned = re.sub(r"[\s\-().]", "", raw.strip())
    if cleaned.startswith("00"):
        cleaned = "+" + cleaned[2:]
    if not _PHONE_RE.match(cleaned):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Phone number must be international format, e.g. +491701234567",
        )
    return cleaned


def _hash_code(code: str) -> str:
    return hashlib.sha256(code.encode()).hexdigest()


def _aware(dt: datetime) -> datetime:
    """SQLite returns naive datetimes; treat stored values as UTC."""
    return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt


def request_code(db: Session, user: User, raw_phone: str) -> None:
    phone = normalize_phone(raw_phone)

    taken = db.query(User).filter(User.phone_number == phone, User.id != user.id).first()
    if taken is not None:
        raise HTTPException(status.HTTP_409_CONFLICT, "Phone number already in use")

    latest = (
        db.query(SmsVerification)
        .filter(SmsVerification.user_id == user.id)
        .order_by(SmsVerification.created_at.desc(), SmsVerification.id.desc())
        .first()
    )
    if latest is not None:
        elapsed = (utcnow() - _aware(latest.created_at)).total_seconds()
        if elapsed < settings.SMS_RESEND_COOLDOWN_SECONDS:
            raise HTTPException(
                status.HTTP_429_TOO_MANY_REQUESTS,
                "Please wait before requesting another code",
            )

    # a new request invalidates all previous pending codes
    db.query(SmsVerification).filter(
        SmsVerification.user_id == user.id, SmsVerification.verified_at.is_(None)
    ).delete()

    code = f"{secrets.randbelow(1_000_000):06d}"
    db.add(
        SmsVerification(
            user_id=user.id,
            phone_number=phone,
            code_hash=_hash_code(code),
            expires_at=utcnow() + timedelta(minutes=settings.SMS_CODE_TTL_MINUTES),
        )
    )
    get_sms_backend().send(phone, CODE_MESSAGE.format(code=code))


def verify_code(db: Session, user: User, code: str) -> User:
    challenge = (
        db.query(SmsVerification)
        .filter(SmsVerification.user_id == user.id, SmsVerification.verified_at.is_(None))
        .order_by(SmsVerification.created_at.desc(), SmsVerification.id.desc())
        .first()
    )
    if challenge is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "No pending code — request one first")
    if _aware(challenge.expires_at) < utcnow():
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Code expired — request a new one")
    if challenge.attempts >= settings.SMS_MAX_ATTEMPTS:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Too many attempts — request a new code")

    if _hash_code(code.strip()) != challenge.code_hash:
        challenge.attempts += 1
        # Commit NOW: the request session rolls back on exceptions, which
        # would erase the attempt counter and defeat the attempt cap.
        db.commit()
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid code")

    # final uniqueness guard (the unique constraint backstops races)
    taken = (
        db.query(User)
        .filter(User.phone_number == challenge.phone_number, User.id != user.id)
        .first()
    )
    if taken is not None:
        raise HTTPException(status.HTTP_409_CONFLICT, "Phone number already in use")

    challenge.verified_at = utcnow()
    user.phone_number = challenge.phone_number
    user.phone_verified_at = utcnow()
    return user
