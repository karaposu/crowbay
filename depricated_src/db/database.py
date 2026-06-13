# db/database.py

from sqlalchemy import create_engine

# Example: local SQLite file named crowd.db (rename as needed)
SQLITE_DB_URL = "sqlite:///./db/data/crowd.db"

engine = create_engine(
    SQLITE_DB_URL,
    connect_args={"check_same_thread": False},
    echo=False
)
