import inspect
import re
from datetime import datetime
from inspect import Parameter, Signature
from typing import Dict, List, Optional, Union

import news.crawlers.db.schema
import news.crawlers.ntdtv
import news.crawlers.util.normalize


def test_module_function_signature() -> None:
    r"""Ensure module functions' signature."""
    assert hasattr(news.crawlers.ntdtv, 'get_datetime_from_url')
    assert inspect.isfunction(news.crawlers.ntdtv.get_datetime_from_url)
    assert inspect.signature(
        news.crawlers.ntdtv.get_datetime_from_url,
    ) == Signature(
        parameters=[
            Parameter(
                name='url',
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Parameter.empty,
                annotation=str,
            ),
        ],
        return_annotation=Union[datetime, None],
    )
    assert hasattr(news.crawlers.ntdtv, 'get_max_page')
    assert inspect.isfunction(news.crawlers.ntdtv.get_max_page)
    assert inspect.signature(
        news.crawlers.ntdtv.get_max_page,
    ) == Signature(
        parameters=[
            Parameter(
                name='category_api',
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Parameter.empty,
                annotation=str,
            ),
            Parameter(
                name='kwargs',
                kind=Parameter.VAR_KEYWORD,
                default=Parameter.empty,
                annotation=Optional[Dict],
            ),
        ],
        return_annotation=int,
    )
    assert hasattr(news.crawlers.ntdtv, 'get_start_page')
    assert inspect.isfunction(news.crawlers.ntdtv.get_start_page)
    assert inspect.signature(
        news.crawlers.ntdtv.get_start_page,
    ) == Signature(
        parameters=[
            Parameter(
                name='category_api',
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Parameter.empty,
                annotation=str,
            ),
            Parameter(
                name='current_datetime',
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Parameter.empty,
                annotation=datetime,
            ),
            Parameter(
                name='max_page',
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Parameter.empty,
                annotation=int,
            ),
            Parameter(
                name='past_datetime',
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Parameter.empty,
                annotation=datetime,
            ),
            Parameter(
                name='continue_fail_count',
                kind=Parameter.KEYWORD_ONLY,
                default=5,
                annotation=Optional[int],
            ),
            Parameter(
                name='debug',
                kind=Parameter.KEYWORD_ONLY,
                default=False,
                annotation=Optional[bool],
            ),
            Parameter(
                name='first_page',
                kind=Parameter.KEYWORD_ONLY,
                default=1,
                annotation=Optional[int],
            ),
            Parameter(
                name='kwargs',
                kind=Parameter.VAR_KEYWORD,
                default=Parameter.empty,
                annotation=Optional[Dict],
            ),
        ],
        return_annotation=int,
    )
    assert hasattr(news.crawlers.ntdtv, 'get_news_list')
    assert inspect.isfunction(news.crawlers.ntdtv.get_news_list)
    assert inspect.signature(
        news.crawlers.ntdtv.get_news_list,
    ) == Signature(
        parameters=[
            Parameter(
                name='category_api',
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Parameter.empty,
                annotation=str,
            ),
            Parameter(
                name='current_datetime',
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Parameter.empty,
                annotation=datetime,
            ),
            Parameter(
                name='first_page',
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Parameter.empty,
                annotation=int,
            ),
            Parameter(
                name='last_page',
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Parameter.empty,
                annotation=int,
            ),
            Parameter(
                name='past_datetime',
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Parameter.empty,
                annotation=datetime,
            ),
            Parameter(
                name='continue_fail_count',
                kind=Parameter.KEYWORD_ONLY,
                default=5,
                annotation=Optional[int],
            ),
            Parameter(
                name='debug',
                kind=Parameter.KEYWORD_ONLY,
                default=False,
                annotation=Optional[bool],
            ),
            Parameter(
                name='kwargs',
                kind=Parameter.VAR_KEYWORD,
                default=Parameter.empty,
                annotation=Optional[Dict],
            ),
        ],
        return_annotation=List[news.crawlers.db.schema.RawNews],
    )
    assert hasattr(news.crawlers.ntdtv, 'main')
    assert inspect.isfunction(news.crawlers.ntdtv.main)
    assert inspect.signature(news.crawlers.ntdtv.main) == Signature(
        parameters=[
            Parameter(
                name='current_datetime',
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Parameter.empty,
                annotation=datetime,
            ),
            Parameter(
                name='db_name',
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Parameter.empty,
                annotation=str,
            ),
            Parameter(
                name='past_datetime',
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Parameter.empty,
                annotation=datetime,
            ),
            Parameter(
                name='kwargs',
                kind=Parameter.VAR_KEYWORD,
                default=Parameter.empty,
                annotation=Optional[Dict],
            ),
        ],
        return_annotation=None,
    )


def test_module_attribute_signature() -> None:
    r"""Ensure module attributes' signature."""
    assert hasattr(news.crawlers.ntdtv, 'CATEGORY_API_LOOKUP_TABLE')
    assert news.crawlers.ntdtv.CATEGORY_API_LOOKUP_TABLE == {
        '國際': '202',
        '港澳': '205',
        '財經': '208',
        '健康': '1255',
        '體育': '211',
        '美國': '203',
        '大陸': '204',
        '文史': '647',
    }
    assert hasattr(news.crawlers.ntdtv, 'COMMIT_PAGE_INTERVAL')
    assert news.crawlers.ntdtv.COMMIT_PAGE_INTERVAL == 100
    assert hasattr(news.crawlers.ntdtv, 'COMPANY_ID')
    assert (
        news.crawlers.ntdtv.COMPANY_ID ==
        news.crawlers.util.normalize.get_company_id(company='新唐人')
    )
    assert hasattr(news.crawlers.ntdtv, 'COMPANY_URL')
    assert (
        news.crawlers.ntdtv.COMPANY_URL == news.crawlers.util.normalize
        .get_company_url(company_id=news.crawlers.ntdtv.COMPANY_ID)
    )
    assert hasattr(news.crawlers.ntdtv, 'DATE_PATTERN')
    assert news.crawlers.ntdtv.DATE_PATTERN == re.compile(
        news.crawlers.ntdtv.COMPANY_URL + r'(\d+)/(\d+)/(\d+)/a\d+\.html',
    )
