import sqlite3
from typing import Dict, List, Tuple

import news.merge.db


def dict_factory(
    cursor: sqlite3.Cursor,
    row: Tuple
) -> Dict:
    r'''將執行完sql指令的回傳物件改為dictionary
    '''
    data = {}
    for idx, col in enumerate(cursor.description):
        data[col[0]] = row[idx]
    return data


class AllRecords:
    def __init__(self, db_name: str = None, cur: sqlite3.Cursor = None):
        # 檢查是否有給予`db_name`或是`cur`，如果都沒有則無法進行後續讀取
        if not db_name and cur is None:
            raise ValueError(
                'at least one of `db_name` or `cur` must be provided.'
            )

        sql = 'SELECT * FROM news'

        conn: sqlite3.Connection = None

        self.records: List[Dict] = []

        if db_name:
            conn = news.merge.db.util.get_conn(db_name=db_name)
            # 將`row_factory`回傳的物件改為dictionary，注意!若傳入的參數為cur由於沒有
            # sqlite3.Connection物件因此無法進行此改動
            conn.row_factory = dict_factory
            cur = conn.cursor()

        # 讀取資料庫內容
        self.records = list(cur.execute(sql))

        # 關閉資料庫連線
        if conn is not None:
            conn.close()

    def __getitem__(self, idx: int) -> Dict:
        return self.records[idx]

    def __len__(self) -> int:
        return len(self.records)
