import os

from news.path import DATA_PATH


def get_db_path(db_name: str) -> str:
    r"""給定資料庫檔案名稱, 回傳資料庫檔案完整路徑"""
    # 預設讀取路徑為 `data/raw`.
    return os.path.join(DATA_PATH, 'raw', db_name)
