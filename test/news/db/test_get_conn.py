import os
import sqlite3

import news.db
import news.path


def test_get_conn(db_path: str, cleanup_db_file) -> None:
    try:
        conn = news.db.get_conn(db_path=db_path)

        assert isinstance(conn, sqlite3.Connection)
        assert os.path.exists(db_path)
    finally:
        conn.close()
