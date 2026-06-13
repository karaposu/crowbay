# filepath: src/db/seed.py

"""Idempotent reference data for the verification system.

Run from src/:  python -m db.seed   (or: make seed)
"""

from sqlalchemy.orm import Session

from db.engine import SessionLocal
from db.models import ProofType, VerificationProofRequirement, VerificationType

PROOF_TYPES = [
    {
        "proof_name": "government_id_photo",
        "proof_category": "document",
        "description": "Clear photo of a government-issued ID "
        "(passport, national ID, driver's license).",
        "file_requirements": {"formats": ["jpg", "jpeg", "png"], "max_mb": 10},
        "extraction_capabilities": [
            "full_name",
            "birth_date",
            "gender",
            "nationality",
            "document_number",
        ],
    },
    {
        "proof_name": "selfie_video",
        "proof_category": "biometric",
        "description": "Short video selfie following the prompted random gesture.",
        "file_requirements": {"formats": ["mp4", "mov", "webm"], "max_mb": 50, "max_seconds": 15},
        "extraction_capabilities": [
            "face_embedding",
            "age_estimate",
            "gender_estimate",
            "liveness_score",
        ],
    },
]

VERIFICATION_TYPES = [
    {
        "verification_name": "basic_identity",
        "tier": 2,
        "description": "User is a real, unique human matching their ID.",
        "expires_after_days": 730,
    },
    {
        "verification_name": "age_verification",
        "tier": 1,
        "description": "Birth date verified.",
        "expires_after_days": None,
    },
    {
        "verification_name": "gender_verification",
        "tier": 1,
        "description": "Gender verified.",
        "expires_after_days": None,
    },
    {
        "verification_name": "location_verification",
        "tier": 1,
        "description": "Country/city of residence verified.",
        "expires_after_days": 365,
    },
]

# (verification_name, proof_name, is_mandatory, alternative_group)
# alternative_group=None -> required (AND); same group number -> any one suffices (OR)
REQUIREMENTS = [
    ("basic_identity", "government_id_photo", True, None),
    ("basic_identity", "selfie_video", True, None),
    ("age_verification", "government_id_photo", True, 1),
    ("age_verification", "selfie_video", True, 1),
    ("gender_verification", "government_id_photo", True, 1),
    ("gender_verification", "selfie_video", True, 1),
    ("location_verification", "government_id_photo", True, None),
]


def seed(session: Session) -> dict[str, int]:
    added = {"proof_types": 0, "verification_types": 0, "requirements": 0}

    for pt in PROOF_TYPES:
        if not session.query(ProofType).filter_by(proof_name=pt["proof_name"]).first():
            session.add(ProofType(**pt))
            added["proof_types"] += 1

    for vt in VERIFICATION_TYPES:
        exists = (
            session.query(VerificationType)
            .filter_by(verification_name=vt["verification_name"])
            .first()
        )
        if not exists:
            session.add(VerificationType(**vt))
            added["verification_types"] += 1

    session.flush()

    for vname, pname, mandatory, group in REQUIREMENTS:
        vt = session.query(VerificationType).filter_by(verification_name=vname).one()
        pt = session.query(ProofType).filter_by(proof_name=pname).one()
        exists = (
            session.query(VerificationProofRequirement)
            .filter_by(verification_type_id=vt.id, proof_type_id=pt.id)
            .first()
        )
        if not exists:
            session.add(
                VerificationProofRequirement(
                    verification_type_id=vt.id,
                    proof_type_id=pt.id,
                    is_mandatory=mandatory,
                    alternative_group=group,
                )
            )
            added["requirements"] += 1

    return added


def main() -> None:
    session = SessionLocal()
    try:
        added = seed(session)
        session.commit()
        print(f"Seed complete: {added}")
    finally:
        session.close()


if __name__ == "__main__":
    main()
