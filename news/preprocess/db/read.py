import sqlite3
from typing import List

import news.preprocess.db
from news.parse.db.schema import ParsedNews


class AllRecords:
    def __init__(self, db_name: str, cur: sqlite3.Cursor = None):
        if not db_name and cur is None:
            raise ValueError(
                'at least one of `db_name` or `cur` must be provided.'
            )

        sql = '''
            SELECT article, category, company_id, datetime, reporter, title, url_pattern
            FROM news
        '''
        conn: sqlite3.Connection = None

        self.records: List[ParsedNews] = []

        if db_name:
            conn = news.preprocess.db.util.get_conn(db_name=db_name)
            cur = conn.cursor()

        for (
            article, category, company_id, datetime,
            reporter, title, url_pattern
        ) in cur.execute(sql):
            self.records.append(ParsedNews(
                article=article,
                category=category,
                company_id=company_id,
                datetime=datetime,
                reporter=reporter,
                title=title,
                url_pattern=url_pattern,
            ))

        if conn is not None:
            conn.close()

    def __getitem__(self, idx: int) -> ParsedNews:
        return self.records[idx]

    def __len__(self) -> int:
        return len(self.records)
