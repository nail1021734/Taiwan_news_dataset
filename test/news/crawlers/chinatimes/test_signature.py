import inspect
from datetime import datetime
from inspect import Parameter, Signature
from typing import Dict, Final, List, Optional

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
                    annotation=Final[datetime],
                ),
                Parameter(
                    name='continue_fail_count',
                    kind=Parameter.KEYWORD_ONLY,
                    default=1000,
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
                    default=100000,
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
    assert hasattr(news.crawlers.chinatimes, 'main')
    assert inspect.isfunction(news.crawlers.chinatimes.main)
    assert (
        inspect.signature(news.crawlers.chinatimes.main) == Signature(
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
    assert hasattr(news.crawlers.chinatimes, 'CATEGORY_ID_LOOKUP_TABLE')
    assert (
        news.crawlers.chinatimes.CATEGORY_ID_LOOKUP_TABLE == {
            '政治': '260407',
            '時尚、玩食': '260405',
            '財經': '260410',
            '社會': '260402',
            '哈燒日韓、西洋熱門': '260404',
            '兩岸': '260409',
            '球類': '260403',
            '國際': '260408',
            '寶島': '260421',
            '科技': '260412',
            '健康': '260418',
            '運勢': '260423',
            '軍事': '260417',
            '新消息': '262301',
            '中時社論': '262101',
            '旺報社評': '262102',
            '工商社論': '262113',
            '快評': '262103',
            '時論廣場': '262104',
            '尚青論壇': '262114',
            '兩岸徵文': '262106',
            '兩岸史話': '262107',
            '海納百川': '262110',
            '消費': '260113',
            '華人星光': '262404',
            '高爾夫': '260111',
            '萌寵': '260819',
            '搜奇': '260809',
            '歷史': '260812',
            '時人真話': '260102',
        }
    )
    assert hasattr(news.crawlers.chinatimes, 'COMPANY_ID')
    assert (
        news.crawlers.chinatimes.COMPANY_ID ==
        news.crawlers.util.normalize.get_company_id(company='中時')
    )
    assert hasattr(news.crawlers.chinatimes, 'COMPANY_URL')
    assert (
        news.crawlers.chinatimes.COMPANY_URL == news.crawlers.util.normalize
        .get_company_url(company_id=news.crawlers.chinatimes.COMPANY_ID,)
    )
