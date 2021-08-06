import sqlite3


def create_table(cur: sqlite3.Cursor):
    cur.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY,
            company_id INTEGER,
            raw_xml TEXT,
            url_pattern TEXT
        );
    """)
