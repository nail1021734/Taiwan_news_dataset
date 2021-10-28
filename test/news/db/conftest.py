import os

import pytest

import news.path


@pytest.fixture
def db_path(db_name: str) -> str:
    return os.path.abspath(os.path.join(news.path.DATA_PATH, 'test', db_name))


@pytest.fixture
def cleanup_db_file(db_path: str, request) -> None:
    r"""Delete testing database files."""

    def remove():
        db_dir = os.path.abspath(os.path.join(db_path, os.pardir))

        if os.path.exists(db_path):
            os.remove(db_path)

        if os.path.exists(db_dir) and not os.listdir(db_dir):
            os.removedirs(db_dir)

    request.addfinalizer(remove)
