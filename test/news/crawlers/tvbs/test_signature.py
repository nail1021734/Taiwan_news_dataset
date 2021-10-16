import inspect
from inspect import Parameter, Signature
from typing import Dict, Final, List, Optional

import news.crawlers.db.schema
import news.crawlers.tvbs
import news.crawlers.util.normalize


def test_module_function_signature() -> None:
    r"""Ensure module functions' signature."""
    assert hasattr(news.crawlers.tvbs, 'get_latest_available_news_idx')
    assert inspect.isfunction(news.crawlers.tvbs.get_latest_available_news_idx)
    assert inspect.signature(
        news.crawlers.tvbs.get_latest_available_news_idx,
    ) == Signature(
        parameters=[
            Parameter(
                name='category',
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
        return_annotation=int,
    )
    assert hasattr(news.crawlers.tvbs, 'get_all_available_news_idx')
    assert inspect.isfunction(news.crawlers.tvbs.get_all_available_news_idx)
    assert inspect.signature(
        news.crawlers.tvbs.get_all_available_news_idx,
    ) == Signature(
        parameters=[
            Parameter(
                name='category',
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
        return_annotation=List[int],
    )
    assert hasattr(news.crawlers.tvbs, 'get_news_list')
    assert inspect.isfunction(news.crawlers.tvbs.get_news_list)
    assert inspect.signature(news.crawlers.tvbs.get_news_list) == Signature(
        parameters=[
            Parameter(
                name='ava_news_idxs',
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Parameter.empty,
                annotation=Final[List[int]],
            ),
            Parameter(
                name='category',
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Parameter.empty,
                annotation=Final[str],
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
    assert hasattr(news.crawlers.tvbs, 'main')
    assert inspect.isfunction(news.crawlers.tvbs.main)
    assert inspect.signature(news.crawlers.tvbs.main) == Signature(
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


def test_module_attribute_signature() -> None:
    r"""Ensure module attributes' signature."""
    assert hasattr(news.crawlers.tvbs, 'CATEGORY_API_LOOKUP_TABLE')
    assert news.crawlers.tvbs.CATEGORY_API_LOOKUP_TABLE == {
        'local': '1',
        'life': '2',
        'world': '3',
        'entertainment': '5',
        'china': '6',
        'politics': '7',
        'sports': '8',
        'tech': '12',
        'focus': '41',
        'fun': '50',
        'travel': '260',
        'health': '262',
        'cars': '269',
        'money': '270',
    }
    assert hasattr(news.crawlers.tvbs, 'COMPANY_ID')
    assert (
        news.crawlers.tvbs.COMPANY_ID ==
        news.crawlers.util.normalize.get_company_id(company='tvbs')
    )
    assert hasattr(news.crawlers.tvbs, 'COMPANY_URL')
    assert (
        news.crawlers.tvbs.COMPANY_URL == news.crawlers.util.normalize
        .get_company_url(company_id=news.crawlers.tvbs.COMPANY_ID,)
    )
