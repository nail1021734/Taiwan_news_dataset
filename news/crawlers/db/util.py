import os
import sqlite3
from typing import Final


PROJECT_ROOT: Final[str] = os.path.abspath(os.path.join(
    os.path.abspath(__file__),
    os.pardir,
    os.pardir,
    os.pardir,
    os.pardir,
))

# 預設讀取路徑的root為`data/raw`
DATA_PATH: Final[str] = os.path.join(PROJECT_ROOT, 'data', 'raw')


def get_path(db_name: str) -> str:
    r'''給定資料庫檔案名稱，回傳資料庫檔案完整路徑
    '''
    return os.path.join(DATA_PATH, db_name)


def get_conn(db_name: str) -> sqlite3.Connection:
    r'''取得資料庫的connection，如果指定的資料庫路徑不存在，
    則創建路徑與檔案後回傳connection
    '''
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
