import inspect
from datetime import datetime
from inspect import Parameter, Signature
from typing import Dict, Final, List, Optional

import news.crawlers.cna
import news.crawlers.db.schema
import news.crawlers.util.normalize


def test_module_function_signature() -> None:
    r"""Ensure module functions' signature."""
    assert hasattr(news.crawlers.cna, 'get_news_list')
    assert inspect.isfunction(news.crawlers.cna.get_news_list)
    assert (
        inspect.signature(news.crawlers.cna.get_news_list) == Signature(
            parameters=[
                Parameter(
                    name='current_datetime',
                    kind=Parameter.POSITIONAL_OR_KEYWORD,
                    default=Parameter.empty,
                    annotation=Final[datetime],
                ),
                Parameter(
                    name='continue_fail_count',
                    kind=Parameter.KEYWORD_ONLY,
                    default=100,
                    annotation=Final[Optional[int]],
                ),
                Parameter(
                    name='debug',
                    kind=Parameter.KEYWORD_ONLY,
                    default=False,
                    annotation=Final[Optional[bool]],
                ),
                Parameter(
                    name='max_news_per_day',
                    kind=Parameter.KEYWORD_ONLY,
                    default=10000,
                    annotation=Final[Optional[int]],
                ),
                Parameter(
                    name='kwargs',
                    kind=Parameter.VAR_KEYWORD,
                    default=Parameter.empty,
                    annotation=Final[Optional[Dict]],
                ),
            ],
            return_annotation=List[news.crawlers.db.schema.RawNews],
        )
    )
    assert hasattr(news.crawlers.cna, 'main')
    assert inspect.isfunction(news.crawlers.cna.main)
    assert (
        inspect.signature(news.crawlers.cna.main) == Signature(
            parameters=[
                Parameter(
                    name='current_datetime',
                    kind=Parameter.POSITIONAL_OR_KEYWORD,
                    default=Parameter.empty,
                    annotation=Final[datetime],
                ),
                Parameter(
                    name='db_name',
                    kind=Parameter.POSITIONAL_OR_KEYWORD,
                    default=Parameter.empty,
                    annotation=Final[str],
                ),
                Parameter(
                    name='past_datetime',
                    kind=Parameter.POSITIONAL_OR_KEYWORD,
                    default=Parameter.empty,
                    annotation=Final[datetime],
                ),
                Parameter(
                    name='kwargs',
                    kind=Parameter.VAR_KEYWORD,
                    default=Parameter.empty,
                    annotation=Final[Optional[Dict]],
                ),
            ],
            return_annotation=None,
        )
    )


def test_module_attribute_signature() -> None:
    r"""Ensure module attributes' signature."""
    assert hasattr(news.crawlers.cna, 'COMPANY_ID')
    assert (
        news.crawlers.cna.COMPANY_ID ==
        news.crawlers.util.normalize.get_company_id(company='中央社')
    )
    assert hasattr(news.crawlers.cna, 'COMPANY_URL')
    assert (
        news.crawlers.cna.COMPANY_URL == news.crawlers.util.normalize
        .get_company_url(company_id=news.crawlers.cna.COMPANY_ID,)
    )
