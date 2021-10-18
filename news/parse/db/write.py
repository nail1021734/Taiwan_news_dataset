import sqlite3
from typing import Final, Sequence

import news.parse.db.schema

READ_SQL: Final[str] = """
    SELECT company_id, url_pattern
    FROM   parsed_news;
"""

WRITE_SQL: Final[str] = """
    INSERT INTO parsed_news(
        article, category, company_id, datetime, reporter, title, url_pattern
    )
    VALUES (
        ?      , ?       , ?         , ?       , ?       , ?    , ?
    );
"""


def write_new_records(
    cur: Final[sqlite3.Cursor],
    news_list: Final[Sequence[news.parse.db.schema.ParsedNews]],
) -> None:
    r"""透過目標資料庫的 `cursor` 將 `news_list` 內的資料保存到目標資料庫中."""

    # 取出已存在目標資料庫的 `company_id` 與 `url_pattern`, 避免重複保存相同的資料.
    # 由於不同新聞網站的新聞經過 `news.crawlers.util.normalize.compress_url` 可能產生
    # 相同的 `url_pattern`, 需要額外使用 `company_id` 做進一步的區隔.
    existed_data = list(cur.execute(READ_SQL))
    existed_data = set(map(lambda row: (row[0], row[1]), existed_data))

    # 過濾掉 `news_list` 內重複的資料並取出 `idx` 以外的欄位.
    res = []
    for n in news_list:
        if n.url_pattern not in existed_data:
            res.append(
                (
                    n.article,
                    n.category,
                    n.company_id,
                    n.datetime,
                    n.reporter,
                    n.title,
                    n.url_pattern,
                )
            )
            existed_data.add((n.company_id, n.url_pattern))

    cur.executemany(WRITE_SQL, res)
