import sqlite3
from typing import Final, Sequence

import news.crawlers.db.schema

READ_SQL: Final[str] = """
    SELECT url_pattern
    FROM   news;
"""

WRITE_SQL: Final[str] = """
    INSERT INTO news(company_id, raw_xml, url_pattern)
    VALUES          (?         , ?      , ?          );
"""


def write_new_records(
    cur: Final[sqlite3.Cursor],
    news_list: Final[Sequence[news.crawlers.db.schema.RawNews]],
) -> None:
    r"""透過目標資料庫的 `cursor` 將 `news_list` 內的資料保存到目標資料庫中."""

    # 取出已存在目標資料庫的 `url_pattern`, 避免重複保存相同的資料.
    existed_url = list(cur.execute(READ_SQL))
    existed_url = set(map(lambda url: url[0], existed_url))

    # 過濾掉 `news_list` 內重複的資料並取出 `idx` 以外的欄位.
    res = []
    for n in news_list:
        if n.url_pattern not in existed_url:
            res.append((
                n.company_id,
                n.raw_xml,
                n.url_pattern,
            ))
            existed_url.add(n.url_pattern)

    cur.executemany(WRITE_SQL, res)
