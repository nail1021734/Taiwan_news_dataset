import sqlite3
from typing import List


def create_table(cur: sqlite3.Cursor, columns: List[str]):
    r"""若指定的資料庫內沒有名為 news 的 table, 則建立 news table"""
    # 根據輸入決定table格式
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
