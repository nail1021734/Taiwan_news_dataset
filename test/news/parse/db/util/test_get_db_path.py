import os

import news.parse.db.util
import news.path


def test_abs_path(db_name: str) -> None:
    r"""Must return same path when input absolute path."""
    assert news.parse.db.util.get_db_path(
        db_name=news.path.PROJECT_ROOT,
    ) == news.path.PROJECT_ROOT


def test_rel_path(db_name: str) -> None:
    r"""Must return absolute path of SQLite database file."""
    db_path = news.parse.db.util.get_db_path(db_name=db_name)

    assert isinstance(db_name, str)
    assert os.path.isabs(db_path)
    assert 'data/parsed' in db_path
