import sqlite3
from typing import Sequence

import news.crawlers.db.schema

SQL: str = """
    INSERT INTO raw_news(company_id, raw_xml, url_pattern)
    VALUES              (?         , ?      , ?          );
"""


def write_new_records(
    cur: sqlite3.Cursor,
    news_list: Sequence[news.crawlers.db.schema.RawNews],
) -> None:
    r"""透過目標資料庫的 `cursor` 將 `news_list` 內的資料保存到目標資料庫中."""
    # 根據 `news.crawlers.db.create.SQL` 的設計, 寫入資料庫時會自動過濾掉
    # `news_list` 內重複的資料. 寫入資料庫時我們取出 `idx` 以外的所有欄位.
    cur.executemany(
        SQL,
        [(
            n.company_id,
            n.raw_xml,
            n.url_pattern,
        ) for n in news_list],
    )
