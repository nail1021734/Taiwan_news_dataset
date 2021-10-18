from typing import Final

import news.db
import news.parse.db.create
import news.parse.db.util


def test_create_table(db_name: Final[str], cleanup_db_file: Final) -> None:
    try:
        db_path = news.parse.db.util.get_db_path(db_name=db_name)
        conn = news.db.get_conn(db_path=db_path)
        cur = conn.cursor()
        # No error is good.
        news.parse.db.create.create_table(cur=cur)
        conn.commit()
    finally:
        conn.close()
