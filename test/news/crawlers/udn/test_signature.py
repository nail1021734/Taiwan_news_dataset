import inspect
from datetime import datetime
from inspect import Parameter, Signature
from typing import Dict, List, Optional

import news.crawlers.db.schema
import news.crawlers.udn
import news.crawlers.util.normalize


def test_module_function_signature() -> None:
    r"""Ensure module functions' signature."""
    assert hasattr(news.crawlers.udn, 'get_last_available_page')
    assert inspect.isfunction(news.crawlers.udn.get_last_available_page)
    assert inspect.signature(
        news.crawlers.udn.get_last_available_page,
    ) == Signature(
        parameters=[
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
        return_annotation=int,
    )
    assert hasattr(news.crawlers.udn, 'get_last_vaild_page')
    assert inspect.isfunction(news.crawlers.udn.get_last_vaild_page)
    assert inspect.signature(
        news.crawlers.udn.get_last_vaild_page,
    ) == Signature(
        parameters=[
            Parameter(
                name='last_ava_page',
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
                name='kwargs',
                kind=Parameter.VAR_KEYWORD,
                default=Parameter.empty,
                annotation=Optional[Dict],
            ),
        ],
        return_annotation=int,
    )
    assert hasattr(news.crawlers.udn, 'get_first_vaild_page')
    assert inspect.isfunction(news.crawlers.udn.get_first_vaild_page)
    assert inspect.signature(
        news.crawlers.udn.get_first_vaild_page,
    ) == Signature(
        parameters=[
            Parameter(
                name='last_valid_page',
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Parameter.empty,
                annotation=int,
            ),
            Parameter(
                name='current_datetime',
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
        return_annotation=int,
    )
    assert hasattr(news.crawlers.udn, 'get_news_list')
    assert inspect.isfunction(news.crawlers.udn.get_news_list)
    assert inspect.signature(news.crawlers.udn.get_news_list) == Signature(
        parameters=[
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
    assert hasattr(news.crawlers.udn, 'main')
    assert inspect.isfunction(news.crawlers.udn.main)
    assert inspect.signature(news.crawlers.udn.main) == Signature(
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
                name='commit_page_interval',
                kind=Parameter.KEYWORD_ONLY,
                default=10,
                annotation=Optional[int],
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
    assert hasattr(news.crawlers.udn, 'COMPANY_ID')
    assert (
        news.crawlers.udn.COMPANY_ID ==
        news.crawlers.util.normalize.get_company_id(company='聯合報')
    )
    assert hasattr(news.crawlers.udn, 'COMPANY_URL')
    assert (
        news.crawlers.udn.COMPANY_URL == news.crawlers.util.normalize
        .get_company_url(company_id=news.crawlers.udn.COMPANY_ID,)
    )
