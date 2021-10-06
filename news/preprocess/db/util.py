import os
import sqlite3
from typing import Final

from news.path import PROJECT_ROOT

# 預設讀取路徑的root為`data/preprocess`
DATA_PATH: Final[str] = os.path.join(PROJECT_ROOT, 'data', 'preprocess')


def get_path(db_name: str) -> str:
    r"""給定資料庫檔案名稱, 回傳資料庫檔案完整路徑"""
    return os.path.join(DATA_PATH, db_name)


def get_conn(db_name: str) -> sqlite3.Connection:
    r"""取得與資料庫的連線

    如果指定的資料庫路徑不存在, 則創建路徑與檔案後回傳連線
    """
    db_path = get_path(db_name)
    db_dir = os.path.dirname(db_path)

    # Create database directory if not exists.
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    # Create database file if not exists.
    if not os.path.exists(db_path):
        open(db_path, 'wb').close()

    if os.path.exists(db_path) and not os.path.isfile(db_path):
        raise FileExistsError(f'{db_path} is not file.')

    return sqlite3.connect(db_path)
