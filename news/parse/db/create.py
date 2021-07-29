import sqlite3


def create_table(cur: sqlite3.Cursor):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY,
            article TEXT,
            category TEXT,
            company_id INTEGER,
            datetime INTEGER,
            reporter TEXT,
            title TEXT,
            url_pattern TEXT
        );
    """)
