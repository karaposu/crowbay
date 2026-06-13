# filepath: src/db/deps.py

from collections.abc import Generator

from sqlalchemy.orm import Session

from db.engine import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """Request-scoped session: commit on success, rollback on error, always close."""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
