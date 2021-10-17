import os
from typing import Final

import news.path


def get_db_path(db_name: Final[str]) -> str:
    r"""給定資料庫檔案名稱, 回傳資料庫檔案完整路徑."""
    # 預設讀取路徑為 `data/parsed`.
    return os.path.join(news.path.DATA_PATH, 'parsed', db_name)
