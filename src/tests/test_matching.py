# filepath: src/tests/test_matching.py

"""Evaluator tests (matching C1) + seeding (C10) + regions (C5)."""

from datetime import date

from db.models import User
from services import matching
from services.attributes import (
    FIELD_BIRTH_DATE,
    FIELD_CITY,
    FIELD_COUNTRY,
    FIELD_GENDER,
    grant_verified_attributes,
    load_snapshot,
)
from services.regions import resolve_region


def _user(db, email: str, **attrs) -> User:
    user = User(email=email)
    db.add(user)
    db.flush()
    if attrs:
        grant_verified_attributes(db, user, attrs)
    db.commit()
    return user


def _birth(age_years: int) -> str:
    today = date.today()
    return today.replace(year=today.year - age_years).isoformat()


def FILTERS(**basic) -> dict:
    return {"basic_filters": basic}


def both_modes(db, filters, user) -> bool:
    """Assert SQL mode and snapshot mode agree, return the verdict."""
    ok, _unmet = matching.user_matches(db, filters, user.id)
    q, _ = matching.audience_query(db, filters)
    in_set = any(u.id == user.id for u in q.all())
    assert ok == in_set, f"snapshot={ok} but sql={in_set} for {filters}"
    return ok


# --- seeding & regions ----------------------------------------------------


def test_grant_and_snapshot(db_session):
    user = _user(
        db_session,
        "snap@x.com",
        **{FIELD_COUNTRY: "Germany", FIELD_CITY: "Berlin", FIELD_GENDER: "Female"},
    )
    snap = load_snapshot(db_session, user.id)
    assert snap[FIELD_COUNTRY] == {"germany"}  # normalized lowercase
    assert snap[FIELD_GENDER] == {"female"}


def test_regrant_supersedes(db_session):
    user = _user(db_session, "regrant@x.com", **{FIELD_COUNTRY: "germany"})
    grant_verified_attributes(db_session, user, {FIELD_COUNTRY: "france"})
    db_session.commit()
    assert load_snapshot(db_session, user.id)[FIELD_COUNTRY] == {"france"}


def test_low_confidence_rows_dont_count(db_session):
    user = _user(db_session, "lowconf@x.com")
    grant_verified_attributes(db_session, user, {FIELD_GENDER: "female"}, confidence=0.5)
    db_session.commit()
    assert FIELD_GENDER not in load_snapshot(db_session, user.id)


def test_region_resolution():
    assert "germany" in resolve_region("EMEA")
    assert "germany" in resolve_region("emea")
    assert "united states" not in resolve_region("emea")
    assert resolve_region("DACH") == ["austria", "germany", "switzerland"]
    assert resolve_region("narnia") is None


# --- evaluator semantics ----------------------------------------------------


def test_no_filters_matches_everyone(db_session):
    user = _user(db_session, "anyone@x.com")  # zero attributes
    assert both_modes(db_session, None, user)
    assert both_modes(db_session, {}, user)


def test_gender_filter(db_session):
    f = _user(db_session, "f@x.com", **{FIELD_GENDER: "female"})
    m = _user(db_session, "m@x.com", **{FIELD_GENDER: "male"})
    nobody = _user(db_session, "n@x.com")

    filters = FILTERS(gender="Female")
    assert both_modes(db_session, filters, f)
    assert not both_modes(db_session, filters, m)
    assert not both_modes(db_session, filters, nobody)  # absence is failure


def test_age_range_with_boundaries(db_session):
    aged = {
        17: _user(db_session, "a17@x.com", **{FIELD_BIRTH_DATE: _birth(17)}),
        18: _user(db_session, "a18@x.com", **{FIELD_BIRTH_DATE: _birth(18)}),
        25: _user(db_session, "a25@x.com", **{FIELD_BIRTH_DATE: _birth(25)}),
        26: _user(db_session, "a26@x.com", **{FIELD_BIRTH_DATE: _birth(26)}),
    }
    filters = FILTERS(age_range={"min": 18, "max": 25})
    assert not both_modes(db_session, filters, aged[17])
    assert both_modes(db_session, filters, aged[18])  # inclusive lower bound
    assert both_modes(db_session, filters, aged[25])  # inclusive upper bound
    assert not both_modes(db_session, filters, aged[26])


def test_open_ended_age(db_session):
    young = _user(db_session, "y@x.com", **{FIELD_BIRTH_DATE: _birth(16)})
    adult = _user(db_session, "ad@x.com", **{FIELD_BIRTH_DATE: _birth(40)})
    filters = FILTERS(age_range={"min": 18})
    assert not both_modes(db_session, filters, young)
    assert both_modes(db_session, filters, adult)


def test_location_country_and_city_or_logic(db_session):
    berliner = _user(db_session, "b@x.com", **{FIELD_COUNTRY: "germany", FIELD_CITY: "berlin"})
    istanbulite = _user(db_session, "i@x.com", **{FIELD_COUNTRY: "turkey", FIELD_CITY: "istanbul"})
    parisian = _user(db_session, "p@x.com", **{FIELD_COUNTRY: "france", FIELD_CITY: "paris"})

    filters = FILTERS(
        location_filter={
            "countries": [{"name": "Germany"}],
            "cities": [{"name": "Istanbul"}],
        }
    )
    assert both_modes(db_session, filters, berliner)  # via country entry
    assert both_modes(db_session, filters, istanbulite)  # via city entry
    assert not both_modes(db_session, filters, parisian)


def test_country_with_city_exception(db_session):
    berliner = _user(db_session, "b2@x.com", **{FIELD_COUNTRY: "germany", FIELD_CITY: "berlin"})
    municher = _user(db_session, "m2@x.com", **{FIELD_COUNTRY: "germany", FIELD_CITY: "munich"})
    filters = FILTERS(
        location_filter={"countries": [{"name": "germany", "exceptions": {"cities": ["Berlin"]}}]}
    )
    assert not both_modes(db_session, filters, berliner)
    assert both_modes(db_session, filters, municher)


def test_region_with_country_exception(db_session):
    german = _user(db_session, "de@x.com", **{FIELD_COUNTRY: "germany"})
    russian = _user(db_session, "ru@x.com", **{FIELD_COUNTRY: "russia"})
    american = _user(db_session, "us@x.com", **{FIELD_COUNTRY: "united states"})

    filters = FILTERS(
        location_filter={"regions": [{"name": "EMEA", "exceptions": {"countries": ["Russia"]}}]}
    )
    assert both_modes(db_session, filters, german)
    assert not both_modes(db_session, filters, russian)  # excepted
    assert not both_modes(db_session, filters, american)  # outside region


def test_combined_filters_are_anded(db_session):
    match = _user(
        db_session,
        "match@x.com",
        **{FIELD_COUNTRY: "germany", FIELD_GENDER: "female", FIELD_BIRTH_DATE: _birth(22)},
    )
    wrong_gender = _user(
        db_session,
        "wg@x.com",
        **{FIELD_COUNTRY: "germany", FIELD_GENDER: "male", FIELD_BIRTH_DATE: _birth(22)},
    )
    filters = FILTERS(
        gender="female",
        age_range={"min": 18, "max": 25},
        location_filter={"countries": [{"name": "germany"}]},
    )
    assert both_modes(db_session, filters, match)
    assert not both_modes(db_session, filters, wrong_gender)

    ok, unmet = matching.user_matches(db_session, filters, wrong_gender.id)
    assert not ok and unmet == ["gender"]


def test_raw_only_location_is_advisory(db_session):
    nobody = _user(db_session, "raw@x.com")  # no attributes at all
    filters = FILTERS(location_filter={"raw_statement": "EMEA but not Russia"})
    pf = matching.parse_filters(filters)
    assert matching.WARN_RAW_LOCATION in pf.warnings
    assert both_modes(db_session, filters, nobody)  # constrains nothing


def test_unknown_region_warns_and_is_ignored(db_session):
    german = _user(db_session, "de2@x.com", **{FIELD_COUNTRY: "germany"})
    filters = FILTERS(
        location_filter={"regions": [{"name": "narnia"}], "countries": [{"name": "germany"}]}
    )
    pf = matching.parse_filters(filters)
    assert any("narnia" in w for w in pf.warnings)
    assert both_modes(db_session, filters, german)  # country entry still works


def test_audience_count_excludes_launcher(db_session):
    _user(db_session, "c1@x.com", **{FIELD_GENDER: "female"})
    launcher = _user(db_session, "c2@x.com", **{FIELD_GENDER: "female"})
    count, _ = matching.audience_count(db_session, FILTERS(gender="female"))
    assert count == 2
    count, _ = matching.audience_count(
        db_session, FILTERS(gender="female"), exclude_user_id=launcher.id
    )
    assert count == 1


def test_garbage_filters_dont_crash(db_session):
    user = _user(db_session, "g@x.com")
    for junk in ("string", 42, {"basic_filters": "nope"}, {"basic_filters": {"age_range": "x"}}):
        ok, _ = matching.user_matches(db_session, junk, user.id)
        assert ok  # nothing parseable = unconstrained
