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

DATA_PATH: Final[str] = os.path.join(PROJECT_ROOT, 'data')


def get_path(db_name: str) -> str:
    return os.path.join(DATA_PATH, db_name)


def get_conn(db_name: str) -> sqlite3.Connection:
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
