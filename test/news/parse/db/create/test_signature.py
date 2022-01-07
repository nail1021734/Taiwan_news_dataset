import inspect
import re
import sqlite3
from inspect import Parameter, Signature

import news.parse.db.create


def test_module_function_signature() -> None:
    r"""Ensure module functions' signature."""
    assert hasattr(news.parse.db.create, 'create_table')
    assert inspect.isfunction(news.parse.db.create.create_table)
    assert (
        inspect.signature(news.parse.db.create.create_table) == Signature(
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
    assert hasattr(news.parse.db.create, 'SQL')
    assert isinstance(news.parse.db.create.SQL, str)
    assert (
        re.sub(r'\s+', ' ', news.parse.db.create.SQL) == re.sub(
            r'\s+', ' ', """
            CREATE TABLE IF NOT EXISTS parsed_news (
                id          INTEGER  PRIMARY KEY AUTOINCREMENT,
                article     TEXT        NOT NULL,
                category    TEXT    DEFAULT NULL,
                company_id  INTEGER     NOT NULL,
                reporter    TEXT    DEFAULT NULL,
                timestamp   INTEGER     NOT NULL,
                title       TEXT        NOT NULL,
                url_pattern TEXT        NOT NULL,
                UNIQUE(company_id, url_pattern) ON CONFLICT IGNORE
            );
        """
        )
    )
