# filepath: src/routers/phone.py

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from db.deps import get_db
from db.models import User
from routers.deps import get_current_user
from schemas.auth import Msg, PhoneRequestCode, PhoneVerifyCode
from services import audit
from services import phone as phone_service

router = APIRouter(prefix="/auth/phone", tags=["auth"])


@router.post("/request", response_model=Msg)
def request_code(
    body: PhoneRequestCode,
    request: Request,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    phone_service.request_code(db, user, body.phone_number)
    audit.record(
        db,
        "auth.phone_code_requested",
        actor_id=user.id,
        target_type="user",
        target_id=user.id,
        request_id=getattr(request.state, "request_id", None),
    )
    return {"msg": "Verification code sent"}


@router.post("/verify", response_model=Msg)
def verify_code(
    body: PhoneVerifyCode,
    request: Request,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    phone_service.verify_code(db, user, body.code)
    audit.record(
        db,
        "auth.phone_verified",
        actor_id=user.id,
        target_type="user",
        target_id=user.id,
        request_id=getattr(request.state, "request_id", None),
    )
    return {"msg": "Phone verified"}
