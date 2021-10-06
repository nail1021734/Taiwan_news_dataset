import sqlite3
from typing import Final, List

import news
import news.crawlers.db
from news.crawlers.db.schema import RawNews

# 讀取用的 SQL 指令
SQL: Final[str] = """
    SELECT id, company_id, raw_xml, url_pattern
    FROM news;
"""


def read_all_records(db_name: str) -> List[RawNews]:
    r"""讀取指定 `db_name` 中所有的 `RawNews`."""

    # 檢查是否有給予 `db_name`, 如果都沒有則無法進行後續讀取.
    if not isinstance(db_name, str):
        raise TypeError('`db_name` must be an instance of `str`.')
    if not db_name:
        raise ValueError('`db_name` cannot be empty.')

    try:
        db_path: str = news.crawlers.db.util.get_db_path(db_name=db_name)
        conn: sqlite3.Connection = news.db.get_conn(db_path=db_path)
        cur: sqlite3.Cursor = conn.cursor()

        # 確保執行 SQL 時表格已存在
        news.crawlers.db.create.create_table(cur=cur)

        news_list = list(cur.execute(SQL))
    finally:
        # 關閉資料庫連線
        conn.close()

    # 將讀取出的資料轉換為 `RawNews` 物件
    all_records: List[RawNews] = []
    for idx, company_id, raw_xml, url_pattern in news_list:
        all_records.append(RawNews(
            idx=idx,
            company_id=company_id,
            raw_xml=raw_xml,
            url_pattern=url_pattern,
        ))

    return all_records
