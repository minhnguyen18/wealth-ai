import sqlite3
from contextlib import contextmanager
from app.config import DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS prices (
    date    TEXT NOT NULL,
    ticker  TEXT NOT NULL,
    close   REAL NOT NULL,
    PRIMARY KEY (date, ticker)
);

CREATE TABLE IF NOT EXISTS macro (
    date      TEXT NOT NULL,
    series_id TEXT NOT NULL,
    value     REAL,
    PRIMARY KEY (date, series_id)
);

CREATE TABLE IF NOT EXISTS holdings (
    client_id TEXT NOT NULL,
    ticker    TEXT NOT NULL,
    shares    REAL NOT NULL CHECK (shares > 0),
    PRIMARY KEY (client_id, ticker)
);
"""


@contextmanager
def get_conn():
    """Open a connection, commit if everything succeeded, always close."""
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    with get_conn() as conn:
        conn.executescript(SCHEMA)