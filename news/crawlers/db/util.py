import os
from typing import Final

import news.path


def get_db_path(db_name: Final[str]) -> str:
    r"""給定資料庫檔案名稱, 回傳資料庫檔案完整路徑."""

    # Return `db_name` when it is an absolute path.
    if os.path.isabs(db_name):
        return db_name

    # Return `PROJECT_ROOT/data/raw/db_name` when it is an relative path.
    # 預設讀取路徑為 `data/raw`.
    return os.path.join(news.path.DATA_PATH, 'raw', db_name)
