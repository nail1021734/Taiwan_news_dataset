import os

import news.path


def get_db_path(db_name: str) -> str:
    r"""給定資料庫檔案名稱, 回傳資料庫檔案完整路徑."""

    # Return `db_name` when it is an absolute path.
    if os.path.isabs(db_name):
        return db_name

    # Return `PROJECT_ROOT/data/parsed/db_name` when it is an relative path.
    # 預設讀取路徑為 `data/parsed`.
    return os.path.join(news.path.DATA_PATH, 'parsed', db_name)
