import sqlite3


def create_table(cur: sqlite3.Cursor):
    r'''建立raw data格式的欄位(舊版本格式的資料庫會被轉成raw data格式保存)
    '''
    cur.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY,
            company_id INTEGER,
            raw_xml TEXT,
            url_pattern TEXT
        );
    """)
