import os
import sqlite3
from typing import Final


def get_conn(db_path: Final[str]) -> sqlite3.Connection:
    r"""取得與資料庫的連線

    如果指定的資料庫路徑不存在, 則創建路徑與檔案後回傳連線
    """
    db_dir = os.path.dirname(db_path)

    # Create database directory if not exists.
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    if os.path.exists(db_path) and not os.path.isfile(db_path):
        raise FileExistsError(f'{db_path} is not file.')

    # Create sqlite database file and return connection.
    return sqlite3.connect(db_path)
