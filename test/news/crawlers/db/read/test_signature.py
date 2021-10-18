import inspect
import re
from inspect import Parameter, Signature
from typing import Final, List

import news.crawlers.db.read
import news.crawlers.db.schema


def test_module_function_signature() -> None:
    r"""Ensure module functions' signature."""
    assert hasattr(news.crawlers.db.read, 'read_all_records')
    assert inspect.isfunction(news.crawlers.db.read.read_all_records)
    assert (
        inspect.signature(news.crawlers.db.read.read_all_records) == Signature(
            parameters=[
                Parameter(
                    name='db_name',
                    kind=Parameter.POSITIONAL_OR_KEYWORD,
                    default=Parameter.empty,
                    annotation=Final[str],
                ),
            ],
            return_annotation=List[news.crawlers.db.schema.RawNews],
        )
    )


def test_module_attribute_signature() -> None:
    r"""Ensure module attributes' signature."""
    assert hasattr(news.crawlers.db.read, 'SQL')
    assert isinstance(news.crawlers.db.read.SQL, str)
    assert (
        re.sub(r'\s+', ' ', news.crawlers.db.read.SQL) == re.sub(
            r'\s+', ' ', """
            SELECT id, company_id, raw_xml, url_pattern
            FROM   raw_news;
        """
        )
    )
