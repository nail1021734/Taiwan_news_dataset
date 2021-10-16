import inspect
from inspect import Parameter, Signature
from typing import Dict, Final, List, Optional

import news.crawlers.db.schema
import news.crawlers.storm
import news.crawlers.util.normalize


def test_module_function_signature() -> None:
    r"""Ensure module functions' signature."""
    assert hasattr(news.crawlers.storm, 'page_not_found')
    assert inspect.isfunction(news.crawlers.storm.page_not_found)
    assert inspect.signature(news.crawlers.storm.page_not_found) == Signature(
        parameters=[
            Parameter(
                name='raw_xml',
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Parameter.empty,
                annotation=Final[str],
            ),
        ],
        return_annotation=bool,
    )
    assert hasattr(news.crawlers.storm, 'get_news_list')
    assert inspect.isfunction(news.crawlers.storm.get_news_list)
    assert inspect.signature(news.crawlers.storm.get_news_list) == Signature(
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
    assert hasattr(news.crawlers.storm, 'main')
    assert inspect.isfunction(news.crawlers.storm.main)
    assert inspect.signature(news.crawlers.storm.main) == Signature(
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
                default=2000,
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


def test_module_attribute_signature() -> None:
    r"""Ensure module attributes' signature."""
    assert hasattr(news.crawlers.storm, 'COMPANY_ID')
    assert (
        news.crawlers.storm.COMPANY_ID ==
        news.crawlers.util.normalize.get_company_id(company='風傳媒')
    )
    assert hasattr(news.crawlers.storm, 'COMPANY_URL')
    assert (
        news.crawlers.storm.COMPANY_URL == news.crawlers.util.normalize
        .get_company_url(company_id=news.crawlers.storm.COMPANY_ID,)
    )
