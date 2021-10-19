import inspect
import re
from inspect import Parameter, Signature
from typing import Final, List, Optional

import news.parse.db.read
import news.parse.db.schema


def test_module_function_signature() -> None:
    r"""Ensure module functions' signature."""
    assert hasattr(news.parse.db.read, 'read_all_records')
    assert inspect.isfunction(news.parse.db.read.read_all_records)
    assert inspect.signature(
        news.parse.db.read.read_all_records,
    ) == Signature(
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
    assert hasattr(news.parse.db.read, 'read_some_records')
    assert inspect.isfunction(news.parse.db.read.read_some_records)
    assert inspect.signature(
        news.parse.db.read.read_some_records,
    ) == Signature(
        parameters=[
            Parameter(
                name='db_name',
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Parameter.empty,
                annotation=Final[str],
            ),
            Parameter(
                name='limit',
                kind=Parameter.KEYWORD_ONLY,
                default=100,
                annotation=Final[Optional[int]],
            ),
            Parameter(
                name='offset',
                kind=Parameter.KEYWORD_ONLY,
                default=0,
                annotation=Final[Optional[int]],
            ),
        ],
        return_annotation=List[news.parse.db.schema.ParsedNews],
    )
    assert hasattr(news.parse.db.read, 'get_num_of_records')
    assert inspect.isfunction(news.parse.db.read.get_num_of_records)
    assert inspect.signature(
        news.parse.db.read.get_num_of_records,
    ) == Signature(
        parameters=[
            Parameter(
                name='db_name',
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Parameter.empty,
                annotation=Final[str],
            ),
        ],
        return_annotation=int,
    )


def test_module_attribute_signature() -> None:
    r"""Ensure module attributes' signature."""
    assert hasattr(news.parse.db.read, 'READ_ALL_RECORDS_SQL')
    assert isinstance(news.parse.db.read.READ_ALL_RECORDS_SQL, str)
    assert (
        re.sub(r'\s+', ' ', news.parse.db.read.READ_ALL_RECORDS_SQL) == re.sub(
            r'\s+',
            ' ',
            """
            SELECT id, article, category, company_id, datetime, reporter,
                   title, url_pattern
            FROM   parsed_news;
            """,
        )
    )
    assert hasattr(news.parse.db.read, 'READ_SOME_RECORDS_SQL')
    assert isinstance(news.parse.db.read.READ_SOME_RECORDS_SQL, str)
    assert (
        re.sub(
            r'\s+',
            ' ',
            news.parse.db.read.READ_SOME_RECORDS_SQL,
        ) == re.sub(
            r'\s+',
            ' ',
            """
            SELECT id, article, category, company_id, datetime, reporter, title,
                   url_pattern
            FROM   parsed_news
            LIMIT  :limit
            OFFSET :offset;
            """,
        )
    )
    assert hasattr(news.parse.db.read, 'READ_NUM_OF_RECORDS_SQL')
    assert isinstance(news.parse.db.read.READ_NUM_OF_RECORDS_SQL, str)
    assert (
        re.sub(
            r'\s+',
            ' ',
            news.parse.db.read.READ_NUM_OF_RECORDS_SQL,
        ) == re.sub(
            r'\s+',
            ' ',
            """
            SELECT COUNT(id)
            FROM   parsed_news;
            """,
        )
    )
