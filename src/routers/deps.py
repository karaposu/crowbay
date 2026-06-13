# filepath: src/routers/deps.py

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from db.deps import get_db
from db.models import User
from services.auth import TokenPurpose, get_user_from_token

_bearer = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
    db: Session = Depends(get_db),
) -> User:
    if credentials is None:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return get_user_from_token(db, credentials.credentials, TokenPurpose.ACCESS)


def get_verified_user(user: User = Depends(get_current_user)) -> User:
    if not user.is_email_verified:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Email not verified")
    return user
