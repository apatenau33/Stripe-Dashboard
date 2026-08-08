import sqlite3
from contextlib import contextmanager
from datetime import datetime, timezone

DB_PATH = "payments.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS payments (
    id          TEXT PRIMARY KEY,
    created_at  TEXT NOT NULL,
    amount      REAL NOT NULL,
    currency    TEXT NOT NULL,
    status      TEXT NOT NULL,
    description TEXT,
    synced_at   TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_payments_created ON payments(created_at);
"""


@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with get_connection() as conn:
        conn.executescript(SCHEMA)


def upsert_payments(payments):
    """Insert new payments, update existing ones. Safe to run repeatedly."""
    now = datetime.now(timezone.utc).isoformat()

    rows = [
        (
            p.id,
            datetime.fromtimestamp(p.created, tz=timezone.utc).isoformat(),
            p.amount / 100,
            p.currency,
            p.status,
            p.description or "",
            now,
        )
        for p in payments
    ]

    with get_connection() as conn:
        before = conn.execute("SELECT COUNT(*) FROM payments").fetchone()[0]
        conn.executemany(
            """
            INSERT INTO payments (id, created_at, amount, currency, status, description, synced_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                status      = excluded.status,
                description = excluded.description,
                synced_at   = excluded.synced_at
            """,
            rows,
        )
        after = conn.execute("SELECT COUNT(*) FROM payments").fetchone()[0]

    return after - before, len(rows) - (after - before)


def count_payments():
    with get_connection() as conn:
        return conn.execute("SELECT COUNT(*) FROM payments").fetchone()[0]