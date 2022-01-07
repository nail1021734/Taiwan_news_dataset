import inspect
from inspect import Parameter, Signature
from typing import Dict, List, Optional

import news.crawlers.db.schema
import news.crawlers.setn
import news.crawlers.util.normalize


def test_module_function_signature() -> None:
    r"""Ensure module functions' signature."""
    assert hasattr(news.crawlers.setn, 'get_news_list')
    assert inspect.isfunction(news.crawlers.setn.get_news_list)
    assert inspect.signature(news.crawlers.setn.get_news_list) == Signature(
        parameters=[
            Parameter(
                name='category_api',
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Parameter.empty,
                annotation=str,
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
                name='max_page',
                kind=Parameter.KEYWORD_ONLY,
                default=20,
                annotation=Optional[int],
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
    assert hasattr(news.crawlers.setn, 'main')
    assert inspect.isfunction(news.crawlers.setn.main)
    assert inspect.signature(news.crawlers.setn.main) == Signature(
        parameters=[
            Parameter(
                name='db_name',
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
        return_annotation=None,
    )


def test_module_attribute_signature() -> None:
    r"""Ensure module attributes' signature."""
    assert hasattr(news.crawlers.setn, 'CATEGORY_API_LOOKUP_TABLE')
    assert news.crawlers.setn.CATEGORY_API_LOOKUP_TABLE == {
        '政治': '6',
        '社會': '41',
        '國際': '5',
        '生活': '4',
        '健康': '65',
        '運動': '34',
        '汽車': '12',
        '地方': '97',
        '名家': '9',
        '新奇': '42',
        '科技': '7',
        '財經': '2',
        '寵物': '47',
    }
    assert hasattr(news.crawlers.setn, 'COMPANY_ID')
    assert (
        news.crawlers.setn.COMPANY_ID ==
        news.crawlers.util.normalize.get_company_id(company='三立')
    )
    assert hasattr(news.crawlers.setn, 'COMPANY_URL')
    assert (
        news.crawlers.setn.COMPANY_URL == news.crawlers.util.normalize
        .get_company_url(company_id=news.crawlers.setn.COMPANY_ID)
    )
