import sqlite3
from typing import Sequence

import news.parse.db.schema

SQL: str = """
    INSERT INTO parsed_news(
        article, category, company_id, reporter, timestamp, title, url_pattern
    )
    VALUES (
        ?      , ?       , ?         , ?       , ?        , ?    , ?
    );
"""


def write_new_records(
    cur: sqlite3.Cursor,
    news_list: Sequence[news.parse.db.schema.ParsedNews],
) -> None:
    r"""透過目標資料庫的 `cursor` 將 `news_list` 內的資料保存到目標資料庫中."""
    # 根據 `news.parse.db.create.SQL` 的設計, 寫入資料庫時會自動過濾掉
    # `news_list` 內重複的資料. 寫入資料庫時我們取出 `idx` 以外的所有欄位.
    cur.executemany(
        SQL,
        [
            (
                n.article,
                n.category,
                n.company_id,
                n.reporter,
                n.timestamp,
                n.title,
                n.url_pattern,
            ) for n in news_list
        ],
    )
