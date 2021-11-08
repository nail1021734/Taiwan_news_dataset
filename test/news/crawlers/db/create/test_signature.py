import inspect
import re
import sqlite3
from inspect import Parameter, Signature

import news.crawlers.db.create


def test_module_function_signature() -> None:
    r"""Ensure module functions' signature."""
    assert hasattr(news.crawlers.db.create, 'create_table')
    assert inspect.isfunction(news.crawlers.db.create.create_table)
    assert (
        inspect.signature(news.crawlers.db.create.create_table) == Signature(
            parameters=[
                Parameter(
                    name='cur',
                    kind=Parameter.POSITIONAL_OR_KEYWORD,
                    default=Parameter.empty,
                    annotation=sqlite3.Cursor
                ),
            ],
            return_annotation=None,
        )
    )


def test_module_attribute_signature() -> None:
    r"""Ensure module attributes' signature."""
    assert hasattr(news.crawlers.db.create, 'SQL')
    assert isinstance(news.crawlers.db.create.SQL, str)
    assert (
        re.sub(r'\s+', ' ', news.crawlers.db.create.SQL) == re.sub(
            r'\s+', ' ', """
            CREATE TABLE IF NOT EXISTS raw_news (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                company_id  INTEGER NOT NULL,
                raw_xml     TEXT    NOT NULL,
                url_pattern TEXT    NOT NULL,
                UNIQUE(company_id, url_pattern) ON CONFLICT IGNORE
            );
        """
        )
    )
