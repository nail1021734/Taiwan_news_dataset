from typing import Final

import news.db


def test_is_sqlite3_file(db_path: Final[str], cleanup_db_file: Final) -> None:
    assert not news.db.is_sqlite3_file(file_path=db_path)

    try:
        conn = news.db.get_conn(db_path=db_path)
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS test (
                id   INTEGER PRIMARY KEY AUTOINCREMENT,
                test TEXT
            );
            """
        )
        conn.commit()
    finally:
        conn.close()

    assert news.db.is_sqlite3_file(file_path=db_path)
