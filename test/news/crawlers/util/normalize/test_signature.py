import inspect
import re
from inspect import Parameter, Signature
from typing import Final

import news.crawlers.util.normalize


def test_module_function_signature() -> None:
    r"""Ensure module functions' signature."""
    assert hasattr(news.crawlers.util.normalize, 'compress_raw_xml')
    assert inspect.isfunction(news.crawlers.util.normalize.compress_raw_xml)
    assert (
        inspect.signature(news.crawlers.util.normalize.compress_raw_xml)
        ==
        Signature(
            parameters=[
                Parameter(
                    name='raw_xml',
                    kind=Parameter.POSITIONAL_OR_KEYWORD,
                    default=Parameter.empty,
                    annotation=Final[str],
                ),
            ],
            return_annotation=str,
        )
    )
    assert hasattr(news.crawlers.util.normalize, 'compress_url')
    assert inspect.isfunction(news.crawlers.util.normalize.compress_url)
    assert (
        inspect.signature(news.crawlers.util.normalize.compress_url)
        ==
        Signature(
            parameters=[
                Parameter(
                    name='company_id',
                    kind=Parameter.POSITIONAL_OR_KEYWORD,
                    default=Parameter.empty,
                    annotation=Final[int],
                ),
                Parameter(
                    name='url',
                    kind=Parameter.POSITIONAL_OR_KEYWORD,
                    default=Parameter.empty,
                    annotation=Final[str],
                ),
            ],
            return_annotation=str,
        )
    )
    assert hasattr(news.crawlers.util.normalize, 'get_company_id')
    assert inspect.isfunction(news.crawlers.util.normalize.get_company_id)
    assert (
        inspect.signature(news.crawlers.util.normalize.get_company_id)
        ==
        Signature(
            parameters=[
                Parameter(
                    name='company',
                    kind=Parameter.POSITIONAL_OR_KEYWORD,
                    default=Parameter.empty,
                    annotation=Final[str],
                ),
            ],
            return_annotation=int,
        )
    )
    assert hasattr(news.crawlers.util.normalize, 'get_company_url')
    assert inspect.isfunction(news.crawlers.util.normalize.get_company_url)
    assert (
        inspect.signature(news.crawlers.util.normalize.get_company_url)
        ==
        Signature(
            parameters=[
                Parameter(
                    name='company_id',
                    kind=Parameter.POSITIONAL_OR_KEYWORD,
                    default=Parameter.empty,
                    annotation=Final[int],
                ),
            ],
            return_annotation=str,
        )
    )


def test_module_attribute_signature() -> None:
    r"""Ensure module attributes' signature."""
    assert hasattr(
        news.crawlers.util.normalize,
        'COMPANY_ID_LOOKUP_TABLE',
    )
    assert isinstance(
        news.crawlers.util.normalize.COMPANY_ID_LOOKUP_TABLE,
        dict,
    )
    assert (
        news.crawlers.util.normalize.COMPANY_ID_LOOKUP_TABLE
        ==
        {
            '中時': 0,
            '中央社': 1,
            '大紀元': 2,
            '東森': 3,
            '民視': 4,
            '自由': 5,
            '新唐人': 6,
            '三立': 7,
            '風傳媒': 8,
            'tvbs': 9,
            '聯合報': 10,
        }
    )
    assert hasattr(
        news.crawlers.util.normalize,
        'COMPANY_URL_LOOKUP_TABLE',
    )
    assert isinstance(
        news.crawlers.util.normalize.COMPANY_URL_LOOKUP_TABLE,
        dict,
    )
    assert (
        news.crawlers.util.normalize.COMPANY_URL_LOOKUP_TABLE
        ==
        {
            0: r'https://www.chinatimes.com/realtimenews/',
            1: r'https://www.cna.com.tw/',
            2: r'https://www.epochtimes.com/',
            3: r'https://star.ettoday.net/',
            4: r'https://www.ftvnews.com.tw/',
            5: r'https://news.ltn.com.tw/',
            6: r'https://www.ntdtv.com/',
            7: r'https://www.setn.com/',
            8: r'https://www.storm.mg/',
            9: r'https://news.tvbs.com.tw/',
            10: r'https://udn.com/news/',
        }
    )
    assert hasattr(
        news.crawlers.util.normalize,
        'COMPANY_URL_FASTEST_LOOKUP_TABLE',
    )
    assert isinstance(
        news.crawlers.util.normalize.COMPANY_URL_FASTEST_LOOKUP_TABLE,
        list,
    )
    assert (
        news.crawlers.util.normalize.COMPANY_URL_FASTEST_LOOKUP_TABLE
        ==
        [
            r'https://www.chinatimes.com/realtimenews/',
            r'https://www.cna.com.tw/',
            r'https://www.epochtimes.com/',
            r'https://star.ettoday.net/',
            r'https://www.ftvnews.com.tw/',
            r'https://news.ltn.com.tw/',
            r'https://www.ntdtv.com/',
            r'https://www.setn.com/',
            r'https://www.storm.mg/',
            r'https://news.tvbs.com.tw/',
            r'https://udn.com/news/',
        ]
    )
    assert hasattr(
        news.crawlers.util.normalize,
        'URL_PATTERN_FASTEST_LOOKUP_TABLE',
    )
    assert isinstance(
        news.crawlers.util.normalize.URL_PATTERN_FASTEST_LOOKUP_TABLE,
        list,
    )
    assert (
        news.crawlers.util.normalize.URL_PATTERN_FASTEST_LOOKUP_TABLE
        ==
        [
            re.compile(r'https://www.chinatimes.com/realtimenews/'),
            re.compile(r'https://www.cna.com.tw/'),
            re.compile(r'https://www.epochtimes.com/'),
            re.compile(r'https://star.ettoday.net/'),
            re.compile(r'https://www.ftvnews.com.tw/'),
            re.compile(r'https://news.ltn.com.tw/'),
            re.compile(r'https://www.ntdtv.com/'),
            re.compile(r'https://www.setn.com/'),
            re.compile(r'https://www.storm.mg/'),
            re.compile(r'https://news.tvbs.com.tw/'),
            re.compile(r'https://udn.com/news/'),
        ]
    )
    assert hasattr(
        news.crawlers.util.normalize,
        'WHITESPACE_COLLAPSE_PATTERN',
    )
    assert isinstance(
        news.crawlers.util.normalize.WHITESPACE_COLLAPSE_PATTERN,
        re.Pattern,
    )
    assert (
        news.crawlers.util.normalize.WHITESPACE_COLLAPSE_PATTERN.pattern
        ==
        r'\s+'
    )
