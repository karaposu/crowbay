# filepath: src/schemas/user.py

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class NotificationPrefs(BaseModel):
    muted: bool


class NotificationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    event_type: str
    text: str | None
    payload: dict | None
    status: str
    created_at: datetime


class VerificationSummary(BaseModel):
    verification_name: str
    status: str
    expires_at: datetime | None


class UserMe(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str | None  # None for Telegram-native accounts
    name: str | None
    telegram_handle: str | None
    is_email_verified: bool
    phone_number: str | None = None  # set only after OTP verification
    is_phone_verified: bool = False
    notifications_muted: bool = False
    created_at: datetime
    verifications: list[VerificationSummary] = []
    trust_score: float | None = None  # placeholder until the trust component lands
