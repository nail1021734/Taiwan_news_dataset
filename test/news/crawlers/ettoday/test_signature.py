import inspect
from inspect import Parameter, Signature
from typing import Dict, Final, List, Optional

import news.crawlers.db.schema
import news.crawlers.ettoday
import news.crawlers.util.normalize


def test_module_function_signature() -> None:
    r"""Ensure module functions' signature."""
    assert hasattr(news.crawlers.ettoday, 'get_news_list')
    assert inspect.isfunction(news.crawlers.ettoday.get_news_list)
    assert (
        inspect.signature(news.crawlers.ettoday.get_news_list) == Signature(
            parameters=[
                Parameter(
                    name='first_idx',
                    kind=Parameter.POSITIONAL_OR_KEYWORD,
                    default=Parameter.empty,
                    annotation=Final[int],
                ),
                Parameter(
                    name='latest_idx',
                    kind=Parameter.POSITIONAL_OR_KEYWORD,
                    default=Parameter.empty,
                    annotation=Final[int],
                ),
                Parameter(
                    name='continue_fail_count',
                    kind=Parameter.KEYWORD_ONLY,
                    default=500,
                    annotation=Final[Optional[int]],
                ),
                Parameter(
                    name='debug',
                    kind=Parameter.KEYWORD_ONLY,
                    default=False,
                    annotation=Final[Optional[bool]],
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
    assert hasattr(news.crawlers.ettoday, 'main')
    assert inspect.isfunction(news.crawlers.ettoday.main)
    assert (
        inspect.signature(news.crawlers.ettoday.main) == Signature(
            parameters=[
                Parameter(
                    name='db_name',
                    kind=Parameter.POSITIONAL_OR_KEYWORD,
                    default=Parameter.empty,
                    annotation=Final[str],
                ),
                Parameter(
                    name='first_idx',
                    kind=Parameter.POSITIONAL_OR_KEYWORD,
                    default=Parameter.empty,
                    annotation=Final[int],
                ),
                Parameter(
                    name='latest_idx',
                    kind=Parameter.POSITIONAL_OR_KEYWORD,
                    default=Parameter.empty,
                    annotation=Final[int],
                ),
                Parameter(
                    name='records_per_commit',
                    kind=Parameter.KEYWORD_ONLY,
                    default=1000,
                    annotation=Final[Optional[int]],
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
    assert hasattr(news.crawlers.ettoday, 'COMPANY_ID')
    assert (
        news.crawlers.ettoday.COMPANY_ID ==
        news.crawlers.util.normalize.get_company_id(company='東森')
    )
    assert hasattr(news.crawlers.ettoday, 'COMPANY_URL')
    assert (
        news.crawlers.ettoday.COMPANY_URL == news.crawlers.util.normalize
        .get_company_url(company_id=news.crawlers.ettoday.COMPANY_ID,)
    )
