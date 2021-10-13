import sqlite3
from typing import List

import news.preprocess.db
from news.parse.db.schema import ParsedNews


class AllRecords:

    def __init__(self, db_name: str, cur: sqlite3.Cursor = None):
        # 檢查是否有給予db_name或是cursor，如果都沒有則無法進行後續讀取
        if not db_name and cur is None:
            raise ValueError(
                'at least one of `db_name` or `cur` must be provided.'
            )

        # 讀取用的sql指令
        sql = """
            SELECT id, article, category, company_id, datetime, reporter, title, url_pattern
            FROM news
        """
        conn: sqlite3.Connection = None

        self.records: List[ParsedNews] = []

        if db_name:
            conn = news.parse.db.util.get_conn(db_name=db_name)
            cur = conn.cursor()

        # 將讀取出的資料轉換為ParsedNews物件
        for (idx, article, category, company_id, datetime, reporter, title,
             url_pattern) in cur.execute(sql):
            self.records.append(
                ParsedNews(
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

        # 關閉資料庫連線
        if conn is not None:
            conn.close()

    def __getitem__(self, idx: int) -> ParsedNews:
        return self.records[idx]

    def __len__(self) -> int:
        return len(self.records)
