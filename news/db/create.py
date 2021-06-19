import sqlite3


def create_table(cur: sqlite3.Cursor):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY,
            article TEXT,
            category TEXT,
            company TEXT,
            datetime TEXT,
            raw_xml TEXT,
            reporter TEXT,
            title TEXT,
            url TEXT
        );
    """)
