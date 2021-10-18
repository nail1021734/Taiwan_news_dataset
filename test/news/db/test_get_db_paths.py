import os
from typing import Final

import news.db


def test_get_db_paths(db_path: Final[str], cleanup_db_file: Final) -> None:
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

    db_paths = news.db.get_db_paths(
        file_paths=[
            db_path,
            # Source code does not contains db files.
            os.path.join(news.path.PROJECT_ROOT, 'news'),
        ],
    )
    assert db_paths == [db_path]
    assert all(map(os.path.isabs, db_paths))
