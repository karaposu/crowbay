# filepath: src/services/matching.py

"""Filter Expression Evaluator (matching concept 1).

One parser, two evaluation modes that must always agree:
- SQL mode: a predicate over users for set queries (audience count, fan-out)
- snapshot mode: pure-Python eval against one user's attribute snapshot
  (jump gate, task feed) — one DB read per user, then zero queries per task

Semantics per devdocs/filter_design.md: AND across fields, OR within
location entries, exceptions subtract from their parent entry, missing
attribute = no match. A location filter with only a raw_statement is
ADVISORY (decision 1): it constrains nothing and produces a warning.
"""

from dataclasses import dataclass, field
from datetime import date, timedelta

from sqlalchemy import and_, exists, or_, true
from sqlalchemy.orm import Session

from config import settings
from db.models import User, VerificationData
from services.attributes import (
    FIELD_BIRTH_DATE,
    FIELD_CITY,
    FIELD_COUNTRY,
    FIELD_GENDER,
    load_snapshot,
)
from services.regions import resolve_region

WARN_RAW_LOCATION = "Location is free text only — it won't constrain matching until parsed"
WARN_ADVANCED = "Advanced filters are not evaluated yet (deferred)"


@dataclass
class ParsedFilters:
    gender: str | None = None
    # age translated to birth-date bounds (ISO strings, lexicographic-safe)
    birth_latest: str | None = None  # age >= min  ->  birth_date <= this
    birth_earliest: str | None = None  # age <= max  ->  birth_date >= this
    cities: list[str] = field(default_factory=list)
    # (country, [excluded cities]) — direct entries and region expansions
    countries: list[tuple[str, list[str]]] = field(default_factory=list)
    has_location: bool = False
    warnings: list[str] = field(default_factory=list)

    @property
    def is_unconstrained(self) -> bool:
        return not (self.gender or self.birth_latest or self.birth_earliest or self.has_location)


def _years_ago(years: int) -> date:
    today = date.today()
    try:
        return today.replace(year=today.year - years)
    except ValueError:  # Feb 29
        return today.replace(year=today.year - years, day=28)


def _lc(value) -> str:
    return str(value).strip().lower()


def parse_filters(filters: dict | None) -> ParsedFilters:
    pf = ParsedFilters()
    if not isinstance(filters, dict):
        return pf

    basic = filters.get("basic_filters")
    if isinstance(filters.get("advanced_filters"), dict) and filters["advanced_filters"]:
        pf.warnings.append(WARN_ADVANCED)
    if not isinstance(basic, dict):
        return pf

    if basic.get("gender"):
        pf.gender = _lc(basic["gender"])

    age = basic.get("age_range")
    if isinstance(age, dict):
        if isinstance(age.get("min"), int):
            pf.birth_latest = _years_ago(age["min"]).isoformat()
        if isinstance(age.get("max"), int):
            pf.birth_earliest = (_years_ago(age["max"] + 1) + timedelta(days=1)).isoformat()

    loc = basic.get("location_filter")
    if isinstance(loc, dict):
        for entry in loc.get("cities") or []:
            if isinstance(entry, dict) and entry.get("name"):
                pf.cities.append(_lc(entry["name"]))

        def _excluded_cities(entry: dict) -> list[str]:
            exc = entry.get("exceptions") or {}
            return [_lc(c) for c in (exc.get("cities") or []) if c]

        for entry in loc.get("countries") or []:
            if isinstance(entry, dict) and entry.get("name"):
                pf.countries.append((_lc(entry["name"]), _excluded_cities(entry)))

        for entry in loc.get("regions") or []:
            if not (isinstance(entry, dict) and entry.get("name")):
                continue
            countries = resolve_region(entry["name"])
            if countries is None:
                pf.warnings.append(f"Unknown region '{entry['name']}' — entry ignored")
                continue
            exc = entry.get("exceptions") or {}
            excluded_countries = {_lc(c) for c in (exc.get("countries") or []) if c}
            excluded_cities = [_lc(c) for c in (exc.get("cities") or []) if c]
            for country in countries:
                if country not in excluded_countries:
                    pf.countries.append((country, excluded_cities))

        pf.has_location = bool(pf.cities or pf.countries)
        if loc.get("raw_statement") and not pf.has_location:
            pf.warnings.append(WARN_RAW_LOCATION)

    return pf


# --- SQL mode -----------------------------------------------------------


def _confidence_ok():
    return or_(
        VerificationData.confidence_score.is_(None),
        VerificationData.confidence_score >= settings.MATCH_CONFIDENCE_MIN,
    )


def _attr_exists(field_name: str, *value_conds):
    return exists().where(
        VerificationData.user_id == User.id,
        VerificationData.field_name == field_name,
        VerificationData.is_current.is_(True),
        _confidence_ok(),
        *value_conds,
    )


def sql_predicate(pf: ParsedFilters):
    conds = []
    if pf.gender:
        conds.append(_attr_exists(FIELD_GENDER, VerificationData.field_value == pf.gender))

    birth_conds = []
    if pf.birth_latest:
        birth_conds.append(VerificationData.field_value <= pf.birth_latest)
    if pf.birth_earliest:
        birth_conds.append(VerificationData.field_value >= pf.birth_earliest)
    if birth_conds:
        conds.append(_attr_exists(FIELD_BIRTH_DATE, *birth_conds))

    if pf.has_location:
        alternatives = []
        for city in pf.cities:
            alternatives.append(_attr_exists(FIELD_CITY, VerificationData.field_value == city))
        for country, excluded_cities in pf.countries:
            cond = _attr_exists(FIELD_COUNTRY, VerificationData.field_value == country)
            if excluded_cities:
                cond = and_(
                    cond,
                    ~_attr_exists(FIELD_CITY, VerificationData.field_value.in_(excluded_cities)),
                )
            alternatives.append(cond)
        conds.append(or_(*alternatives))

    return and_(*conds) if conds else true()


# --- snapshot mode -------------------------------------------------------


def unmet_requirements(pf: ParsedFilters, snapshot: dict[str, set[str]]) -> list[str]:
    """Which filter fields this snapshot fails. Empty list = match."""
    unmet = []

    if pf.gender and pf.gender not in snapshot.get(FIELD_GENDER, set()):
        unmet.append("gender")

    if pf.birth_latest or pf.birth_earliest:
        births = snapshot.get(FIELD_BIRTH_DATE, set())
        ok = any(
            (pf.birth_latest is None or b <= pf.birth_latest)
            and (pf.birth_earliest is None or b >= pf.birth_earliest)
            for b in births
        )
        if not ok:
            unmet.append("age")

    if pf.has_location:
        user_cities = snapshot.get(FIELD_CITY, set())
        user_countries = snapshot.get(FIELD_COUNTRY, set())
        ok = any(city in user_cities for city in pf.cities) or any(
            country in user_countries and not (user_cities & set(excluded))
            for country, excluded in pf.countries
        )
        if not ok:
            unmet.append("location")

    return unmet


# --- public API ----------------------------------------------------------


def user_matches(db: Session, filters: dict | None, user_id: int) -> tuple[bool, list[str]]:
    """Snapshot-mode check for one user. Returns (ok, unmet field names)."""
    pf = parse_filters(filters)
    if pf.is_unconstrained:
        return True, []
    unmet = unmet_requirements(pf, load_snapshot(db, user_id))
    return not unmet, unmet


def audience_query(db: Session, filters: dict | None):
    """SQL-mode query over matching users. Returns (query, warnings)."""
    pf = parse_filters(filters)
    return db.query(User).filter(sql_predicate(pf)), pf.warnings


def audience_count(
    db: Session, filters: dict | None, exclude_user_id: int | None = None
) -> tuple[int, list[str]]:
    q, warnings = audience_query(db, filters)
    if exclude_user_id is not None:
        q = q.filter(User.id != exclude_user_id)
    return q.count(), warnings
