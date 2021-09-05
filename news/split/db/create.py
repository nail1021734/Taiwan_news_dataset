import sqlite3
from typing import List


def create_table(cur: sqlite3.Cursor, columns: List[str]):
    # 根據輸入決定table格式
    if 'url' in columns:
        # 針對舊資料格式，切割舊資料格式時會用到
        cur.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY,
            article TEXT,
            category TEXT,
            company INTEGER,
            datetime INTEGER,
            reporter TEXT,
            title TEXT,
            url TEXT,
            raw_xml TEXT
        );
        """)
    elif len(columns) == 4:
        # 處理raw data
        cur.execute("""
            CREATE TABLE IF NOT EXISTS news (
                id INTEGER PRIMARY KEY,
                company_id INTEGER,
                raw_xml TEXT,
                url_pattern TEXT
            );
        """)
    else:
        # 處理parse過的data
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
