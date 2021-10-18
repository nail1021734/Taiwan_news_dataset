import sqlite3
from typing import Final, List

import news.db
import news.parse.db.create
import news.parse.db.schema
import news.parse.db.util

# 讀取用的 SQL 指令
SQL: Final[str] = """
    SELECT id, article, category, company_id, datetime, reporter, title,
           url_pattern
    FROM   parsed_news;
"""


def read_all_records(
    db_name: Final[str],
) -> List[news.parse.db.schema.ParsedNews]:
    r"""讀取指定 `db_name` 中所有的 `ParsedNews`."""

    # 檢查是否有給予 `db_name`, 如果都沒有則無法進行後續讀取.
    if not isinstance(db_name, str):
        raise TypeError('`db_name` must be an instance of `str`.')
    if not db_name:
        raise ValueError('`db_name` cannot be empty.')

    try:
        db_path: str = news.parse.db.util.get_db_path(db_name=db_name)
        conn: sqlite3.Connection = news.db.get_conn(db_path=db_path)
        cur: sqlite3.Cursor = conn.cursor()

        # 確保執行 SQL 時表格已存在
        news.parse.db.create.create_table(cur=cur)

        news_list = list(cur.execute(SQL))
    finally:
        # 關閉資料庫連線
        conn.close()

    # 將讀取出的資料轉換為 `ParsedNews` 物件
    all_records: List[news.parse.db.schema.ParsedNews] = []
    for (idx, article, category, company_id, datetime, reporter, title,
         url_pattern) in news_list:
        all_records.append(
            news.parse.db.schema.ParsedNews(
                idx=idx,
                article=article,
                category=category,
                company_id=company_id,
                datetime=datetime,
                reporter=reporter,
                title=title,
                url_pattern=url_pattern,
            )
        )

    return all_records
