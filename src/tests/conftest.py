# filepath: src/tests/conftest.py

import os
import tempfile

# Must happen before config/app import — Settings reads env at import time.
_TMPDIR = tempfile.mkdtemp(prefix="cj_test_")
os.environ["DATABASE_URL"] = f"sqlite:///{_TMPDIR}/test.db"
os.environ.setdefault("SECRET_KEY", "test-secret-key-not-for-production-0000000000")
os.environ.setdefault("BOT_BRIDGE_SECRET", "test-bridge-secret")

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

import db.models  # noqa: F401, E402  (register tables on Base.metadata)
from app import app  # noqa: E402
from db.base import Base  # noqa: E402
from db.engine import SessionLocal, engine  # noqa: E402

Base.metadata.create_all(engine)


@pytest.fixture(autouse=True)
def _clean_db():
    """Each test starts from an empty database."""
    yield
    with engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(table.delete())


@pytest.fixture()
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture()
def db_session():
    s = SessionLocal()
    yield s
    s.close()


@pytest.fixture()
def register(client):
    """Returns a helper: register(email) -> (auth headers, token pair)."""

    def _register(email: str, password: str = "password1234"):
        r = client.post("/auth/register", json={"email": email, "password": password})
        assert r.status_code == 201, r.text
        pair = r.json()
        return {"Authorization": f"Bearer {pair['access_token']}"}, pair

    return _register
