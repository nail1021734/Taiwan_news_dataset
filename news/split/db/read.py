import sqlite3
from typing import Dict, List

import news.split.db


def dict_factory(
    cursor: sqlite3.Cursor,
    row
):
    data = {}
    for idx, col in enumerate(cursor.description):
        data[col[0]] = row[idx]
    return data


class AllRecords:
    def __init__(
        self,
        offset: int,
        interval: int,
        db_name: str = None,
        cur: sqlite3.Cursor = None,
    ):
        if not db_name and cur is None:
            raise ValueError(
                'at least one of `db_name` or `cur` must be provided.'
            )

        sql = f'SELECT * FROM news LIMIT {interval} OFFSET {offset}'

        conn: sqlite3.Connection = None

        self.records: List[Dict] = []

        if db_name:
            conn = news.split.db.util.get_conn(db_name=db_name)
            # Notice!! when use `cur` parameter this line will not work(not return dictionary).
            conn.row_factory = dict_factory
            cur = conn.cursor()
        self.records = list(cur.execute(sql))

        if conn is not None:
            conn.close()

    def __getitem__(self, idx: int) -> Dict:
        return self.records[idx]

    def __len__(self) -> int:
        return len(self.records)
