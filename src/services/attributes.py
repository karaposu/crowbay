# filepath: src/services/attributes.py

"""Verified-attribute access + dev seeding (concept 10).

CANONICAL ATTRIBUTE NAMES — the contract between the future verification
component (writer) and matching (reader). Mismatched names fail silently,
so both sides must import from here:

    location_country   lowercase English country name ("germany")
    location_city      lowercase city name ("berlin")
    birth_date         ISO date ("1999-05-01")
    gender             lowercase ("female", "male", ...)
"""

from sqlalchemy.orm import Session

from config import settings
from db.base import utcnow
from db.models import User, UserVerification, VerificationData, VerificationType

FIELD_COUNTRY = "location_country"
FIELD_CITY = "location_city"
FIELD_BIRTH_DATE = "birth_date"
FIELD_GENDER = "gender"

KNOWN_FIELDS = (FIELD_COUNTRY, FIELD_CITY, FIELD_BIRTH_DATE, FIELD_GENDER)

DEV_SEED_VERIFICATION = "dev_seed"


def load_snapshot(db: Session, user_id: int) -> dict[str, set[str]]:
    """All current, confident attribute values for a user: field -> values.

    NULL confidence counts as confident — the row exists because a
    verification accepted it; the score is optional metadata.
    """
    rows = (
        db.query(VerificationData.field_name, VerificationData.field_value)
        .filter(
            VerificationData.user_id == user_id,
            VerificationData.is_current.is_(True),
            (VerificationData.confidence_score.is_(None))
            | (VerificationData.confidence_score >= settings.MATCH_CONFIDENCE_MIN),
        )
        .all()
    )
    snapshot: dict[str, set[str]] = {}
    for field, value in rows:
        snapshot.setdefault(field, set()).add(value.strip().lower())
    return snapshot


def grant_verified_attributes(
    db: Session, user: User, attrs: dict[str, str], confidence: float = 1.0
) -> None:
    """DEV/TEST ONLY: write verified attributes without the real pipeline.

    Creates (once) a 'dev_seed' verification type + a verified
    UserVerification for the user, then current VerificationData rows.
    Existing current rows for the same field are superseded (is_current=False),
    matching how the real pipeline will behave.
    """
    vtype = db.query(VerificationType).filter_by(verification_name=DEV_SEED_VERIFICATION).first()
    if vtype is None:
        vtype = VerificationType(
            verification_name=DEV_SEED_VERIFICATION,
            tier=0,
            description="Development-seeded attributes (not a real verification).",
            expires_after_days=None,
        )
        db.add(vtype)
        db.flush()

    user_verification = (
        db.query(UserVerification).filter_by(user_id=user.id, verification_type_id=vtype.id).first()
    )
    if user_verification is None:
        user_verification = UserVerification(
            user_id=user.id,
            verification_type_id=vtype.id,
            status="verified",
            completed_at=utcnow(),
        )
        db.add(user_verification)
        db.flush()

    for field, value in attrs.items():
        db.query(VerificationData).filter(
            VerificationData.user_id == user.id,
            VerificationData.field_name == field,
            VerificationData.is_current.is_(True),
        ).update({"is_current": False})
        db.add(
            VerificationData(
                user_id=user.id,
                field_name=field,
                field_value=value.strip().lower(),
                verification_source_id=user_verification.id,
                confidence_score=confidence,
                is_current=True,
            )
        )
