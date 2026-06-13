# filepath: src/routers/auth.py

import secrets

from fastapi import APIRouter, Depends, Header, HTTPException, Query, Request
from sqlalchemy.orm import Session

from config import settings
from db.deps import get_db
from db.models import User
from routers.deps import get_current_user
from schemas.auth import (
    LoginRequest,
    Msg,
    PasswordResetConfirm,
    PasswordResetRequest,
    RefreshRequest,
    RegisterRequest,
    TelegramBridgeRequest,
    TokenPair,
)
from services import audit, emailer
from services import auth as auth_service
from services.auth import TokenPurpose

router = APIRouter(prefix="/auth", tags=["auth"])


def _request_id(request: Request) -> str | None:
    return getattr(request.state, "request_id", None)


@router.post("/register", response_model=TokenPair, status_code=201)
def register(body: RegisterRequest, request: Request, db: Session = Depends(get_db)) -> dict:
    user = auth_service.register_user(db, body.email, body.password)
    emailer.send_verification_email(user.email, auth_service.create_email_verify_token(user.id))
    audit.record(
        db,
        "auth.register",
        actor_id=user.id,
        target_type="user",
        target_id=user.id,
        request_id=_request_id(request),
    )
    return auth_service.token_pair(user.id)


@router.post("/login", response_model=TokenPair)
def login(body: LoginRequest, request: Request, db: Session = Depends(get_db)) -> dict:
    user = auth_service.authenticate(db, body.email, body.password)
    audit.record(
        db,
        "auth.login",
        actor_id=user.id,
        target_type="user",
        target_id=user.id,
        request_id=_request_id(request),
    )
    return auth_service.token_pair(user.id)


@router.post("/refresh", response_model=TokenPair)
def refresh(body: RefreshRequest, db: Session = Depends(get_db)) -> dict:
    user = auth_service.get_user_from_token(db, body.refresh_token, TokenPurpose.REFRESH)
    return auth_service.token_pair(user.id)


@router.get("/verify-email", response_model=Msg)
def verify_email(token: str = Query(...), db: Session = Depends(get_db)) -> dict:
    user = auth_service.get_user_from_token(db, token, TokenPurpose.EMAIL_VERIFY)
    user.is_email_verified = True  # idempotent
    return {"msg": "Email verified"}


@router.post("/request-password-reset", response_model=Msg)
def request_password_reset(body: PasswordResetRequest, db: Session = Depends(get_db)) -> dict:
    # Always 200 — response must not reveal whether the account exists.
    email = auth_service.normalize_email(body.email)
    user = db.query(User).filter(User.email == email).first()
    if user is not None:
        emailer.send_password_reset_email(user.email, auth_service.create_pw_reset_token(user.id))
    return {"msg": "If the account exists, a reset email was sent"}


@router.post("/reset-password", response_model=Msg)
def reset_password(body: PasswordResetConfirm, db: Session = Depends(get_db)) -> dict:
    user = auth_service.get_user_from_token(db, body.token, TokenPurpose.PW_RESET)
    user.password_hash = auth_service.hash_password(body.new_password)
    return {"msg": "Password reset"}


@router.post("/resend-verification", response_model=Msg)
def resend_verification(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> dict:
    if user.email is None:
        raise HTTPException(400, "This account has no email address")
    if user.is_email_verified:
        return {"msg": "Email already verified"}
    emailer.send_verification_email(user.email, auth_service.create_email_verify_token(user.id))
    return {"msg": "Verification email sent"}


@router.post("/telegram", response_model=TokenPair)
def telegram_bridge(
    body: TelegramBridgeRequest,
    request: Request,
    db: Session = Depends(get_db),
    x_bridge_secret: str = Header(alias="X-Bridge-Secret"),
) -> dict:
    """Trusted bot->API bridge: authenticate a user by Telegram identity.

    Only the bot knows the bridge secret; end users never call this.
    """
    if settings.BOT_BRIDGE_SECRET is None:
        raise HTTPException(503, "Telegram bridge is not configured")
    if not secrets.compare_digest(x_bridge_secret, settings.BOT_BRIDGE_SECRET):
        raise HTTPException(401, "Invalid bridge secret")

    user, created = auth_service.bridge_telegram_user(db, body.telegram_id, body.telegram_handle)
    audit.record(
        db,
        "auth.telegram_bridge",
        actor_id=user.id,
        target_type="user",
        target_id=user.id,
        payload={"created": created},
        request_id=_request_id(request),
    )
    return auth_service.token_pair(user.id)
