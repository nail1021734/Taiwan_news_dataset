r"""創建資料表儲存爬蟲結果.

資料表共包含 4 個欄位:

+-------------+---------+---------------------------+
| column      | type    | constraint                |
+=============+=========+===========================+
| id          | INTEGER | PRIMARY KEY AUTOINCREMENT |
+-------------+---------+---------------------------+
| company_id  | INTEGER | NOT NULL                  |
+-------------+---------+---------------------------+
| raw_xml     | TEXT    | NOT NULL                  |
+-------------+---------+---------------------------+
| url_pattern | TEXT    | NOT NULL                  |
+-------------+---------+---------------------------+

其中 id 為流水號, company_id 代表新聞網站, raw_xml 代表新聞網頁原始碼,
url_pattern 代表該新聞網頁的 url 格式.
每筆資料都是從某個新聞網站 (company_id) 中的某個頁面 (url_pattern) 抓取下來的
網頁原始碼 (raw_xml).
"""

import sqlite3

# We use unique constraint to avoid duplicated records.  When inserting
# duplicated records, we simply ignore them.
SQL: str = """
    CREATE TABLE IF NOT EXISTS raw_news (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id  INTEGER NOT NULL,
        raw_xml     TEXT    NOT NULL,
        url_pattern TEXT    NOT NULL,
        UNIQUE(company_id, url_pattern) ON CONFLICT IGNORE
    );
"""


def create_table(cur: sqlite3.Cursor) -> None:
    r"""執行創建表格 SQL."""
    cur.execute(SQL)
