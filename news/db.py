import os
import sqlite3
from typing import List, Sequence


def get_conn(db_path: str) -> sqlite3.Connection:
    r"""取得與資料庫的連線

    如果指定的資料庫路徑不存在, 則創建路徑與檔案後回傳連線
    """
    db_dir = os.path.dirname(db_path)

    if os.path.exists(db_path) and not os.path.isfile(db_path):
        raise FileExistsError(f'{db_path} is not file.')

    # Create database directory if not exists.
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    # Create SQLite database file and return connection.
    return sqlite3.connect(db_path)


def is_sqlite3_file(file_path: str) -> bool:
    r"""Return True if `file_path` is SQLite database file.

    Return False when `file_path` is not an absolute path since we did not know
    where the file is located.

    See source_ for design details.

    .. _source: https://stackoverflow.com/questions/12932607/how-to-check-if-a
        -sqlite3-database-exists-in-python
    """
    if not os.path.isabs(file_path):
        return False
    if not os.path.isfile(file_path):
        return False

    # SQLite database file header is 100 bytes. See
    # https://www.sqlite.org/fileformat.html for more information.
    if os.path.getsize(file_path) < 100:
        return False

    try:
        with open(file_path, 'rb') as f:
            header = f.read(100)

        return header[:16] == b'SQLite format 3\x00'
    # Do not have read permission.
    except Exception:
        return False


def get_db_paths(file_paths: Sequence[str]) -> List[str]:
    r"""Recursively search all file paths to find SQLite database files.

    Only absolute paths in `file_paths` will be considered.  Relative paths are
    discard by default since we did not know where the file is located.
    """
    db_paths = []
    for file_path in file_paths:
        # Recursively walk through directories.
        if os.path.isdir(file_path):
            for root, _, file_names in os.walk(file_path):
                for file_name in file_names:
                    abs_file_path = os.path.join(root, file_name)
                    if is_sqlite3_file(file_path=abs_file_path):
                        db_paths.append(abs_file_path)
        elif is_sqlite3_file(file_path=file_path):
            db_paths.append(file_path)

    return db_paths
