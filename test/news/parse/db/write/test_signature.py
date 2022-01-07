import inspect
import re
import sqlite3
from inspect import Parameter, Signature
from typing import Sequence

import news.parse.db.write
from news.parse.db.schema import ParsedNews


def test_module_function_signature() -> None:
    r"""Ensure module functions' signature."""
    assert hasattr(news.parse.db.write, 'write_new_records')
    assert inspect.isfunction(news.parse.db.write.write_new_records)
    assert inspect.signature(news.parse.db.write.write_new_records) \
        == Signature(
            parameters=[
                Parameter(
                    name='cur',
                    kind=Parameter.POSITIONAL_OR_KEYWORD,
                    default=Parameter.empty,
                    annotation=sqlite3.Cursor,
                ),
                Parameter(
                    name='news_list',
                    kind=Parameter.POSITIONAL_OR_KEYWORD,
                    default=Parameter.empty,
                    annotation=Sequence[ParsedNews],
                ),
            ],
            return_annotation=None,
        )


def test_module_attribute_signature() -> None:
    r"""Ensure module attributes' signature."""
    assert hasattr(news.parse.db.write, 'SQL')
    assert isinstance(news.parse.db.write.SQL, str)
    assert (
        re.sub(r'\s+', ' ', news.parse.db.write.SQL) == re.sub(
            r'\s+', ' ', """
                INSERT INTO parsed_news(
                    article, category, company_id, reporter, timestamp, title,
                    url_pattern
                )
                VALUES (
                    ?      , ?       , ?         , ?       , ?        , ?    ,
                    ?
                );
            """
        )
    )
