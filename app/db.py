import sqlite3
import os

DB_PATH = os.environ.get("DB_PATH", "/data/legami.db")


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_conn() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS subscribers (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                email     TEXT    NOT NULL UNIQUE,
                token     TEXT    NOT NULL UNIQUE,
                created_at TEXT   NOT NULL DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS known_skus (
                sku        TEXT PRIMARY KEY,
                first_seen TEXT NOT NULL DEFAULT (datetime('now'))
            );
        """)
