import os
from typing import Final

import news.crawlers.db.util


def test_get_db_path(db_name: Final[str]) -> None:
    r"""Must return absolute path of sqlite database file."""
    db_path = news.crawlers.db.util.get_db_path(db_name=db_name)

    assert isinstance(db_name, str)
    assert os.path.isabs(db_path)
