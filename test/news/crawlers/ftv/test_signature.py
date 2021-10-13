import inspect
from datetime import datetime
from inspect import Parameter, Signature
from typing import Dict, Final, List, Optional

import news.crawlers.db.schema
import news.crawlers.ftv
import news.crawlers.util.normalize


def test_module_function_signature() -> None:
    r"""Ensure module functions' signature."""
    assert hasattr(news.crawlers.ftv, 'page_not_found')
    assert inspect.isfunction(news.crawlers.ftv.page_not_found)
    assert inspect.signature(news.crawlers.ftv.page_not_found) == Signature(
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
    assert hasattr(news.crawlers.ftv, 'get_news_list')
    assert inspect.isfunction(news.crawlers.ftv.get_news_list)
    assert inspect.signature(news.crawlers.ftv.get_news_list) == Signature(
        parameters=[
            Parameter(
                name='category_api',
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Parameter.empty,
                annotation=Final[str],
            ),
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
                name='kwargs',
                kind=Parameter.VAR_KEYWORD,
                default=Parameter.empty,
                annotation=Final[Optional[Dict]],
            ),
        ],
        return_annotation=List[news.crawlers.db.schema.RawNews],
    )
    assert hasattr(news.crawlers.ftv, 'main')
    assert inspect.isfunction(news.crawlers.ftv.main)
    assert inspect.signature(news.crawlers.ftv.main) == Signature(
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


def test_module_attribute_signature() -> None:
    r"""Ensure module attributes' signature."""
    assert hasattr(news.crawlers.ftv, 'CATEGORY_API_LOOKUP_TABLE')
    assert news.crawlers.ftv.CATEGORY_API_LOOKUP_TABLE == {
        'A': '體育',
        'C': '一般',
        'F': '財經',
        'I': '國際',
        'J': '美食',
        'L': '生活',
        'N': '社會',
        'P': '政治',
        'R': '美食',
        'S': '社會',
        'U': '社會',
        'W': '一般',
    }
    assert hasattr(news.crawlers.ftv, 'COMPANY_ID')
    assert (
        news.crawlers.ftv.COMPANY_ID ==
        news.crawlers.util.normalize.get_company_id(company='民視')
    )
    assert hasattr(news.crawlers.ftv, 'COMPANY_URL')
    assert (
        news.crawlers.ftv.COMPANY_URL == news.crawlers.util.normalize
        .get_company_url(company_id=news.crawlers.ftv.COMPANY_ID)
    )
