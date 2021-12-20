r"""創建資料表儲存爬蟲新聞內容處理結果.

資料表共包含 8 個欄位:

+-------------+---------+---------------------------+
| column      | type    | constraint                |
+=============+=========+===========================+
| id          | INTEGER | PRIMARY KEY AUTOINCREMENT |
+-------------+---------+---------------------------+
| article     | TEXT    | NOT NULL                  |
+-------------+---------+---------------------------+
| category    | TEXT    | DEFAULT NULL              |
+-------------+---------+---------------------------+
| company_id  | INTEGER | NOT NULL                  |
+-------------+---------+---------------------------+
| reporter    | TEXT    | DEFAULT NULL              |
+-------------+---------+---------------------------+
| timestamp   | INTEGER | NOT NULL                  |
+-------------+---------+---------------------------+
| title       | TEXT    | NOT NULL                  |
+-------------+---------+---------------------------+
| url_pattern | TEXT    | NOT NULL                  |
+-------------+---------+---------------------------+

每一筆資料都是從 `news.crawlers.db.schema.RawNews` 轉換而來, 因此部份欄位保留原樣,
剩餘欄位為拆解其他欄位所得.
- id 為流水號, 與 `news.crawlers.db.schema.RawNews` 中的 id 不同.
- article 為新聞內文, 從 `news.crawlers.db.schema.RawNews` 中 raw_xml 的部份文字取得.
- category 為新聞內文, 從 `news.crawlers.db.schema.RawNews` 中 raw_xml 或
  url_pattern 的部份文字取得.  部份新聞並沒有類別.
- company_id 代表新聞網站, 與 `news.crawlers.db.schema.RawNews` 中的
  company_id 相同.
- reporter 為新聞記者 (可以是多人, 以逗點區隔), 從 `news.crawlers.db.schema.RawNews`
  中 raw_xml 的部份文字取得.  部份新聞並沒有記者.
- timestamp 為新聞發表日期, 從 `news.crawlers.db.schema.RawNews` 中 raw_xml 或
  url_pattern 的部份文字取得.
- title 為新聞標題, 從 `news.crawlers.db.schema.RawNews` 中 raw_xml 的部份文字取得.
- url_pattern 代表該新聞網頁的 url 格式 與 `news.crawlers.db.schema.RawNews` 中的
  url_pattern 相同.
"""

import sqlite3

SQL: str = """
    CREATE TABLE IF NOT EXISTS parsed_news (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        article     TEXT        NOT NULL,
        category    TEXT    DEFAULT NULL,
        company_id  INTEGER     NOT NULL,
        reporter    TEXT    DEFAULT NULL,
        timestamp   INTEGER     NOT NULL,
        title       TEXT        NOT NULL,
        url_pattern TEXT        NOT NULL,
        UNIQUE(company_id, url_pattern) ON CONFLICT IGNORE
    );
"""


def create_table(cur: sqlite3.Cursor) -> None:
    r"""執行創建表格 SQL."""
    cur.execute(SQL)
