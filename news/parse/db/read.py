import sqlite3
from typing import List, Optional, Tuple

import news.db
import news.parse.db.create
import news.parse.db.schema
import news.parse.db.util

# 讀取用的 SQL 指令
READ_ALL_RECORDS_SQL: str = """
    SELECT id, article, category, company_id, reporter, timestamp, title,
           url_pattern
    FROM   parsed_news;
"""

# 讀取部份資料用的 SQL 指令.
READ_SOME_RECORDS_SQL: str = """
    SELECT id, article, category, company_id, reporter, timestamp, title,
           url_pattern
    FROM   parsed_news
    LIMIT  :limit
    OFFSET :offset;
"""

# 讀取資料數的 SQL 指令.
READ_NUM_OF_RECORDS_SQL: str = """
    SELECT COUNT(id)
    FROM   parsed_news;
"""

# 讀取最小與最大 timestamp 的 SQL 指令.
READ_TIMESTAMP_BOUNDS: str = """
    SELECT MIN(timestamp), MAX(timestamp)
    FROM   parsed_news;
"""


def read_all_records(db_name: str,) -> List[news.parse.db.schema.ParsedNews]:
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

        news_list = list(cur.execute(READ_ALL_RECORDS_SQL))
    finally:
        # 關閉資料庫連線
        conn.close()

    # 將讀取出的資料轉換為 `ParsedNews` 物件
    records: List[news.parse.db.schema.ParsedNews] = []
    for (idx, article, category, company_id, reporter, timestamp, title,
         url_pattern) in news_list:
        records.append(
            news.parse.db.schema.ParsedNews(
                idx=idx,
                article=article,
                category=category,
                company_id=company_id,
                reporter=reporter,
                timestamp=timestamp,
                title=title,
                url_pattern=url_pattern,
            )
        )

    return records


def read_some_records(
    db_name: str,
    *,
    limit: Optional[int] = 100,
    offset: Optional[int] = 0,
) -> List[news.parse.db.schema.ParsedNews]:
    r"""讀取指定 `db_name` 中部份的 `ParsedNews`."""

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
        db_path: str = news.parse.db.util.get_db_path(db_name=db_name)
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

    # 將讀取出的資料轉換為 `ParsedNews` 物件
    records: List[news.parse.db.schema.ParsedNews] = []
    for (idx, article, category, company_id, reporter, timestamp, title,
         url_pattern) in news_list:
        records.append(
            news.parse.db.schema.ParsedNews(
                idx=idx,
                article=article,
                category=category,
                company_id=company_id,
                reporter=reporter,
                timestamp=timestamp,
                title=title,
                url_pattern=url_pattern,
            )
        )

    return records


def get_num_of_records(db_name: str,) -> int:
    r"""讀取指定 `db_name` 中 `ParsedNews` 的資料數."""

    # 檢查是否有給予 `db_name`, 如果都沒有則無法進行後續讀取.
    if not isinstance(db_name, str):
        raise TypeError('`db_name` must be an instance of `str`.')
    if not db_name:
        raise ValueError('`db_name` cannot be empty.')

    try:
        db_path: str = news.parse.db.util.get_db_path(db_name=db_name)
        conn: sqlite3.Connection = news.db.get_conn(db_path=db_path)
        cur: sqlite3.Cursor = conn.cursor()

        num_of_records = list(cur.execute(READ_NUM_OF_RECORDS_SQL))[0][0]
    finally:
        # 關閉資料庫連線
        conn.close()

    return num_of_records


def get_timestamp_bounds(db_name: str,) -> Tuple[int, int]:
    r"""讀取指定 `db_name` 中 `ParsedNews` 的最小與最大 timestamp."""

    # 檢查是否有給予 `db_name`, 如果都沒有則無法進行後續讀取.
    if not isinstance(db_name, str):
        raise TypeError('`db_name` must be an instance of `str`.')
    if not db_name:
        raise ValueError('`db_name` cannot be empty.')

    try:
        db_path: str = news.parse.db.util.get_db_path(db_name=db_name)
        conn: sqlite3.Connection = news.db.get_conn(db_path=db_path)
        cur: sqlite3.Cursor = conn.cursor()

        timestamp_bound = list(cur.execute(READ_TIMESTAMP_BOUNDS))[0]
    finally:
        # 關閉資料庫連線
        conn.close()

    return timestamp_bound
