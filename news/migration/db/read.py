import sqlite3
from typing import List

import news.migration.db
from news.migration.db.schema import OriginNews


class AllRecords:
    def __init__(self, db_name: str, cur: sqlite3.Cursor = None):
        if not db_name and cur is None:
            raise ValueError(
                'at least one of `db_name` or `cur` must be provided.'
            )

        sql = 'SELECT id, company, raw_xml, url FROM news'

        conn: sqlite3.Connection = None

        self.records: List[OriginNews] = []

        if db_name:
            conn = news.migration.db.util.get_conn(db_name=db_name)
            cur = conn.cursor()

        for (
            index, company, raw_xml, url
        ) in cur.execute(sql):
            self.records.append(OriginNews(
                company=company,
                raw_xml=raw_xml,
                url=url,
            ))

        if conn is not None:
            conn.close()

    def __getitem__(self, idx: int) -> OriginNews:
        return self.records[idx]

    def __len__(self) -> int:
        return len(self.records)
