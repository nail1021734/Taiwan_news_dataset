import inspect
import re
from inspect import Parameter, Signature
from typing import Final, List

import news.parse.db.read
import news.parse.db.schema


def test_module_function_signature() -> None:
    r"""Ensure module functions' signature."""
    assert hasattr(news.parse.db.read, 'read_all_records')
    assert inspect.isfunction(news.parse.db.read.read_all_records)
    assert (
        inspect.signature(news.parse.db.read.read_all_records) == Signature(
            parameters=[
                Parameter(
                    name='db_name',
                    kind=Parameter.POSITIONAL_OR_KEYWORD,
                    default=Parameter.empty,
                    annotation=Final[str],
                ),
            ],
            return_annotation=List[news.parse.db.schema.ParsedNews],
        )
    )


def test_module_attribute_signature() -> None:
    r"""Ensure module attributes' signature."""
    assert hasattr(news.parse.db.read, 'SQL')
    assert isinstance(news.parse.db.read.SQL, str)
    assert (
        re.sub(r'\s+', ' ', news.parse.db.read.SQL) == re.sub(
            r'\s+', ' ', """
                SELECT id, article, category, company_id, datetime, reporter,
                    title, url_pattern
                FROM   parsed_news;
            """
        )
    )
