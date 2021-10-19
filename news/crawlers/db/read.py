import sqlite3
from typing import Final, List, Optional

import news.crawlers.db.create
import news.crawlers.db.schema
import news.crawlers.db.util
import news.db

# 讀取全部資料用的 SQL 指令.
READ_ALL_RECORDS_SQL: Final[str] = """
    SELECT id, company_id, raw_xml, url_pattern
    FROM   raw_news;
"""

# 讀取部份資料用的 SQL 指令.
READ_SOME_RECORDS_SQL: Final[str] = """
    SELECT id, company_id, raw_xml, url_pattern
    FROM   raw_news
    LIMIT  :limit
    OFFSET :offset;
"""

# 讀取資料數的 SQL 指令.
READ_NUM_OF_RECORDS_SQL: Final[str] = """
    SELECT COUNT(id)
    FROM   raw_news;
"""


def read_all_records(
    db_name: Final[str],
) -> List[news.crawlers.db.schema.RawNews]:
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

        news_list = list(cur.execute(READ_ALL_RECORDS_SQL))
    finally:
        # 關閉資料庫連線
        conn.close()

    # 將讀取出的資料轉換為 `RawNews` 物件
    records: List[news.crawlers.db.schema.RawNews] = []
    for idx, company_id, raw_xml, url_pattern in news_list:
        records.append(
            news.crawlers.db.schema.RawNews(
                idx=idx,
                company_id=company_id,
                raw_xml=raw_xml,
                url_pattern=url_pattern,
            )
        )

    return records


def read_some_records(
    db_name: Final[str],
    *,
    limit: Final[Optional[int]] = 100,
    offset: Final[Optional[int]] = 0,
) -> List[news.crawlers.db.schema.RawNews]:
    r"""讀取指定 `db_name` 中部份的 `RawNews`."""

    # 檢查是否有給予 `db_name`, 如果都沒有則無法進行後續讀取.
    if not isinstance(db_name, str):
        raise TypeError('`db_name` must be an instance of `str`.')
    if not db_name:
        raise ValueError('`db_name` cannot be empty.')
    if not isinstance(limit, int):
        raise TypeError('`limit` must be an instance of `int`.')
    if limit <= 0:
        raise ValueError('`limit` must be positive integer.')
    if not isinstance(offset, int):
        raise TypeError('`offset` must be an instance of `int`.')
    if offset < 0:
        raise ValueError('`offset` must be non-negative integer.')

    try:
        db_path: str = news.crawlers.db.util.get_db_path(db_name=db_name)
        conn: sqlite3.Connection = news.db.get_conn(db_path=db_path)
        cur: sqlite3.Cursor = conn.cursor()

        news_list = list(
            cur.execute(
                READ_SOME_RECORDS_SQL,
                {
                    'limit': limit,
                    'offset': offset,
                },
            )
        )
    finally:
        # 關閉資料庫連線
        conn.close()

    # 將讀取出的資料轉換為 `RawNews` 物件
    records: List[news.crawlers.db.schema.RawNews] = []
    for idx, company_id, raw_xml, url_pattern in news_list:
        records.append(
            news.crawlers.db.schema.RawNews(
                idx=idx,
                company_id=company_id,
                raw_xml=raw_xml,
                url_pattern=url_pattern,
            )
        )

    return records


def get_num_of_records(db_name: Final[str],) -> int:
    r"""讀取指定 `db_name` 中 `RawNews` 的資料數."""

    # 檢查是否有給予 `db_name`, 如果都沒有則無法進行後續讀取.
    if not isinstance(db_name, str):
        raise TypeError('`db_name` must be an instance of `str`.')
    if not db_name:
        raise ValueError('`db_name` cannot be empty.')

    try:
        db_path: str = news.crawlers.db.util.get_db_path(db_name=db_name)
        conn: sqlite3.Connection = news.db.get_conn(db_path=db_path)
        cur: sqlite3.Cursor = conn.cursor()

        num_of_records = list(cur.execute(READ_NUM_OF_RECORDS_SQL))[0][0]
    finally:
        # 關閉資料庫連線
        conn.close()

    return num_of_records
