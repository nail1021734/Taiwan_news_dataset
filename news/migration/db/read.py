import sqlite3
from typing import List

import news.migration.db
from news.migration.db.schema import OldNews


class AllRecords:

    def __init__(self, db_name: str, cur: sqlite3.Cursor = None):
        # 檢查是否有給予`db_name`或是`cur`，如果都沒有則無法進行後續讀取
        if not db_name and cur is None:
            raise ValueError(
                'at least one of `db_name` or `cur` must be provided.'
            )

        # 讀取用的sql指令
        sql = 'SELECT id, company, raw_xml, url FROM news'

        conn: sqlite3.Connection = None

        self.records: List[OldNews] = []

        if db_name:
            conn = news.migration.db.util.get_conn(db_name=db_name)
            cur = conn.cursor()

        # 將讀取出的資料轉換為OldNews物件
        for (idx, company, raw_xml, url) in cur.execute(sql):
            self.records.append(
                OldNews(
                    idx=idx,
                    company=company,
                    raw_xml=raw_xml,
                    url=url,
                )
            )

        # 關閉資料庫連線
        if conn is not None:
            conn.close()

    def __getitem__(self, idx: int) -> OldNews:
        return self.records[idx]

    def __len__(self) -> int:
        return len(self.records)
