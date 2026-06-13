# filepath: src/db/seed_dev.py

"""DEV ONLY: grant verified attributes to a user so matching is testable
before the verification component exists.

Run from src/:
  python -m db.seed_dev --email jumper@x.com --country germany --city berlin \
      --birth-date 1999-05-01 --gender female
  python -m db.seed_dev --telegram-id 123456 --country turkey
"""

import argparse

from db.engine import SessionLocal
from db.models import User
from services.attributes import (
    FIELD_BIRTH_DATE,
    FIELD_CITY,
    FIELD_COUNTRY,
    FIELD_GENDER,
    grant_verified_attributes,
)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    who = parser.add_mutually_exclusive_group(required=True)
    who.add_argument("--email")
    who.add_argument("--telegram-id")
    parser.add_argument("--country")
    parser.add_argument("--city")
    parser.add_argument("--birth-date", help="ISO date, e.g. 1999-05-01")
    parser.add_argument("--gender")
    args = parser.parse_args()

    attrs = {}
    if args.country:
        attrs[FIELD_COUNTRY] = args.country
    if args.city:
        attrs[FIELD_CITY] = args.city
    if args.birth_date:
        attrs[FIELD_BIRTH_DATE] = args.birth_date
    if args.gender:
        attrs[FIELD_GENDER] = args.gender
    if not attrs:
        parser.error("nothing to grant — pass at least one attribute")

    session = SessionLocal()
    try:
        q = session.query(User)
        user = (
            q.filter(User.email == args.email.lower()).first()
            if args.email
            else q.filter(User.telegram_id == str(args.telegram_id)).first()
        )
        if user is None:
            raise SystemExit("User not found")
        grant_verified_attributes(session, user, attrs)
        session.commit()
        print(f"Granted to user {user.id}: {attrs}")
    finally:
        session.close()


if __name__ == "__main__":
    main()
