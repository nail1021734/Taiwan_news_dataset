import sqlite3


def create_table(cur: sqlite3.Cursor):
    r"""若指定的 database 內沒有名為 news 的 table, 則建立 news table"""
    cur.execute(
        """
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
    """
    )
