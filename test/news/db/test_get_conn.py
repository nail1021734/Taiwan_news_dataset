import os
import sqlite3
from typing import Final

import news.db
import news.path


def test_get_conn(db_path: Final[str], cleanup_db_file: Final) -> None:
    try:
        conn = news.db.get_conn(db_path=db_path)

        assert isinstance(conn, sqlite3.Connection)
        assert os.path.exists(db_path)
    finally:
        conn.close()
