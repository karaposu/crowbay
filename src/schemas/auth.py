# filepath: src/schemas/auth.py

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(min_length=8, max_length=128)


class TelegramBridgeRequest(BaseModel):
    telegram_id: int = Field(gt=0)
    telegram_handle: str | None = Field(default=None, max_length=64)


class PhoneRequestCode(BaseModel):
    # format/semantic validation lives in services.phone.normalize_phone so
    # every malformed number gets the same helpful 400
    phone_number: str = Field(min_length=1, max_length=24)


class PhoneVerifyCode(BaseModel):
    code: str = Field(min_length=4, max_length=10)


class Msg(BaseModel):
    msg: str
