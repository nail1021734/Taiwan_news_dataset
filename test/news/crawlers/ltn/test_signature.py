import inspect
from inspect import Parameter, Signature
from typing import Dict, Final, List, Optional

import news.crawlers.db.schema
import news.crawlers.ltn
import news.crawlers.util.normalize


def test_module_function_signature() -> None:
    r"""Ensure module functions' signature."""
    assert hasattr(news.crawlers.ltn, 'get_news_list')
    assert inspect.isfunction(news.crawlers.ltn.get_news_list)
    assert inspect.signature(news.crawlers.ltn.get_news_list) == Signature(
        parameters=[
            Parameter(
                name='category_api',
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Parameter.empty,
                annotation=Final[str],
            ),
            Parameter(
                name='continue_fail_count',
                kind=Parameter.KEYWORD_ONLY,
                default=5,
                annotation=Final[Optional[int]],
            ),
            Parameter(
                name='debug',
                kind=Parameter.KEYWORD_ONLY,
                default=False,
                annotation=Final[Optional[bool]],
            ),
            Parameter(
                name='first_page',
                kind=Parameter.KEYWORD_ONLY,
                default=1,
                annotation=Final[Optional[int]],
            ),
            Parameter(
                name='max_page',
                kind=Parameter.KEYWORD_ONLY,
                default=25,
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
    assert hasattr(news.crawlers.ltn, 'main')
    assert inspect.isfunction(news.crawlers.ltn.main)
    assert inspect.signature(news.crawlers.ltn.main) == Signature(
        parameters=[
            Parameter(
                name='db_name',
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Parameter.empty,
                annotation=Final[str],
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
    assert hasattr(news.crawlers.ltn, 'CATEGORY_API_LOOKUP_TABLE')
    assert news.crawlers.ltn.CATEGORY_API_LOOKUP_TABLE == {
        '政治': 'politics',
        '社會': 'society',
        '生活': 'life',
        '國際': 'world',
        '地方': 'local',
        '蒐奇': 'novelty',
    }
    assert hasattr(news.crawlers.ltn, 'COMPANY_ID')
    assert (
        news.crawlers.ltn.COMPANY_ID ==
        news.crawlers.util.normalize.get_company_id(company='自由')
    )
    assert hasattr(news.crawlers.ltn, 'COMPANY_URL')
    assert (
        news.crawlers.ltn.COMPANY_URL == news.crawlers.util.normalize
        .get_company_url(company_id=news.crawlers.ltn.COMPANY_ID)
    )
