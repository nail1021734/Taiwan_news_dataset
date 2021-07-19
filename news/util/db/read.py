import sqlite3
from typing import List

import news.util.db
from news.util.db.schema import News


class AllRecords:
    def __init__(self, db_name: str, cur: sqlite3.Cursor = None):
        if not db_name and cur is None:
            raise ValueError(
                'at least one of `db_name` or `cur` must be provided.'
            )

        sql = '''
            SELECT article, category, company, datetime, raw_xml, reporter, title, url
            FROM news
        '''
        conn: sqlite3.Connection = None

        self.records: List[News] = []

        if db_name:
            conn = news.db.util.get_conn(db_name=db_name)
            cur = conn.cursor()

        for (
            article, category, company, datetime, raw_xml,
            reporter, title, url
        ) in cur.execute(sql):
            self.records.append(News(
                article=article,
                category=category,
                company=company,
                datetime=datetime,
                raw_xml=raw_xml,
                reporter=reporter,
                title=title,
                url=url,
            ))

        if conn is not None:
            conn.close()

    def __getitem__(self, idx: int) -> News:
        return self.records[idx]

    def __len__(self) -> int:
        return len(self.records)
