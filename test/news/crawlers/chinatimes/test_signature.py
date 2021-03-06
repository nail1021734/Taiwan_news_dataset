import inspect
from datetime import datetime
from inspect import Parameter, Signature
from typing import Dict, List, Optional

import news.crawlers.chinatimes
import news.crawlers.db.schema
import news.crawlers.util.normalize


def test_module_function_signature() -> None:
    r"""Ensure module functions' signature."""
    assert hasattr(news.crawlers.chinatimes, 'get_news_list')
    assert inspect.isfunction(news.crawlers.chinatimes.get_news_list)
    assert (
        inspect.signature(news.crawlers.chinatimes.get_news_list) == Signature(
            parameters=[
                Parameter(
                    name='current_datetime',
                    kind=Parameter.POSITIONAL_OR_KEYWORD,
                    default=Parameter.empty,
                    annotation=datetime,
                ),
                Parameter(
                    name='continue_fail_count',
                    kind=Parameter.KEYWORD_ONLY,
                    default=1000,
                    annotation=Optional[int],
                ),
                Parameter(
                    name='debug',
                    kind=Parameter.KEYWORD_ONLY,
                    default=False,
                    annotation=Optional[bool],
                ),
                Parameter(
                    name='max_news_per_day',
                    kind=Parameter.KEYWORD_ONLY,
                    default=100000,
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
    )
    assert hasattr(news.crawlers.chinatimes, 'main')
    assert inspect.isfunction(news.crawlers.chinatimes.main)
    assert (
        inspect.signature(news.crawlers.chinatimes.main) == Signature(
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
    )


def test_module_attribute_signature() -> None:
    r"""Ensure module attributes' signature."""
    assert hasattr(news.crawlers.chinatimes, 'CATEGORY_ID_LOOKUP_TABLE')
    assert (
        news.crawlers.chinatimes.CATEGORY_ID_LOOKUP_TABLE == {
            '??????': '260407',
            '???????????????': '260405',
            '??????': '260410',
            '??????': '260402',
            '???????????????????????????': '260404',
            '??????': '260409',
            '??????': '260403',
            '??????': '260408',
            '??????': '260421',
            '??????': '260412',
            '??????': '260418',
            '??????': '260423',
            '??????': '260417',
            '?????????': '262301',
            '????????????': '262101',
            '????????????': '262102',
            '????????????': '262113',
            '??????': '262103',
            '????????????': '262104',
            '????????????': '262114',
            '????????????': '262106',
            '????????????': '262107',
            '????????????': '262110',
            '??????': '260113',
            '????????????': '262404',
            '?????????': '260111',
            '??????': '260819',
            '??????': '260809',
            '??????': '260812',
            '????????????': '260102',
        }
    )
    assert hasattr(news.crawlers.chinatimes, 'COMPANY_ID')
    assert (
        news.crawlers.chinatimes.COMPANY_ID ==
        news.crawlers.util.normalize.get_company_id(company='??????')
    )
    assert hasattr(news.crawlers.chinatimes, 'COMPANY_URL')
    assert (
        news.crawlers.chinatimes.COMPANY_URL == news.crawlers.util.normalize
        .get_company_url(company_id=news.crawlers.chinatimes.COMPANY_ID,)
    )
