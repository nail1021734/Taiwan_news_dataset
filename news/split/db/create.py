import sqlite3
from typing import List


def create_table(cur: sqlite3.Cursor, columns: List[str]):
    if len(columns) == 4:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY,
                company_id INTEGER,
                raw_xml TEXT,
                url_pattern TEXT
            );
        """)
    else:
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
