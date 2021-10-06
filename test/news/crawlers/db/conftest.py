import os

import pytest

import news.crawlers.db.util


@pytest.fixture
def cleanup_db_file(db_name: str, request) -> None:
    r"""Delete testing database files."""

    def remove():
        db_path = news.crawlers.db.util.get_db_path(db_name=db_name)
        db_dir = os.path.abspath(os.path.join(db_path, os.pardir))

        if os.path.exists(db_path):
            os.remove(db_path)

        if os.path.exists(db_dir) and not os.listdir(db_dir):
            os.removedirs(db_dir)

    request.addfinalizer(remove)
