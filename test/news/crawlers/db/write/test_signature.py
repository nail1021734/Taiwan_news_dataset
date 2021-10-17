import inspect
import re
import sqlite3
from inspect import Parameter, Signature
from typing import Final, Sequence

import news.crawlers.db.write
from news.crawlers.db.schema import RawNews


def test_module_function_signature() -> None:
    r"""Ensure module functions' signature."""
    assert hasattr(news.crawlers.db.write, 'write_new_records')
    assert inspect.isfunction(news.crawlers.db.write.write_new_records)
    assert inspect.signature(news.crawlers.db.write.write_new_records) \
        == Signature(
            parameters=[
                Parameter(
                    name='cur',
                    kind=Parameter.POSITIONAL_OR_KEYWORD,
                    default=Parameter.empty,
                    annotation=Final[sqlite3.Cursor],
                ),
                Parameter(
                    name='news_list',
                    kind=Parameter.POSITIONAL_OR_KEYWORD,
                    default=Parameter.empty,
                    annotation=Final[Sequence[RawNews]],
                ),
            ],
            return_annotation=None,
        )


def test_module_attribute_signature() -> None:
    r"""Ensure module attributes' signature."""
    assert hasattr(news.crawlers.db.write, 'READ_SQL')
    assert isinstance(news.crawlers.db.write.READ_SQL, str)
    assert (
        re.sub(r'\s+', ' ', news.crawlers.db.write.READ_SQL) == re.sub(
            r'\s+', ' ', """
            SELECT url_pattern
            FROM   raw_news;
        """
        )
    )
    assert hasattr(news.crawlers.db.write, 'WRITE_SQL')
    assert isinstance(news.crawlers.db.write.WRITE_SQL, str)
    assert (
        re.sub(r'\s+', ' ', news.crawlers.db.write.WRITE_SQL) == re.sub(
            r'\s+', ' ', """
            INSERT INTO raw_news(company_id, raw_xml, url_pattern)
            VALUES              (?         , ?      , ?          );
        """
        )
    )
