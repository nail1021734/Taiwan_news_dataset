import inspect
import re
from inspect import Parameter, Signature

import news.crawlers.util.normalize


def test_module_function_signature() -> None:
    r"""Ensure module functions' signature."""
    assert hasattr(news.crawlers.util.normalize, 'compress_raw_xml')
    assert inspect.isfunction(news.crawlers.util.normalize.compress_raw_xml)
    assert inspect.signature(news.crawlers.util.normalize.compress_raw_xml) \
        == Signature(
            parameters=[
                Parameter(
                    name='raw_xml',
                    kind=Parameter.POSITIONAL_OR_KEYWORD,
                    default=Parameter.empty,
                    annotation=str,
                ),
            ],
            return_annotation=str,
    )
    assert hasattr(news.crawlers.util.normalize, 'compress_url')
    assert inspect.isfunction(news.crawlers.util.normalize.compress_url)
    assert inspect.signature(news.crawlers.util.normalize.compress_url) \
        == Signature(
            parameters=[
                Parameter(
                    name='company_id',
                    kind=Parameter.POSITIONAL_OR_KEYWORD,
                    default=Parameter.empty,
                    annotation=int,
                ),
                Parameter(
                    name='url',
                    kind=Parameter.POSITIONAL_OR_KEYWORD,
                    default=Parameter.empty,
                    annotation=str,
                ),
            ],
            return_annotation=str,
    )
    assert hasattr(news.crawlers.util.normalize, 'get_company_id')
    assert inspect.isfunction(news.crawlers.util.normalize.get_company_id)
    assert inspect.signature(news.crawlers.util.normalize.get_company_id) \
        == Signature(
            parameters=[
                Parameter(
                    name='company',
                    kind=Parameter.POSITIONAL_OR_KEYWORD,
                    default=Parameter.empty,
                    annotation=str,
                ),
            ],
            return_annotation=int,
    )
    assert hasattr(news.crawlers.util.normalize, 'get_company_url')
    assert inspect.isfunction(news.crawlers.util.normalize.get_company_url)
    assert inspect.signature(news.crawlers.util.normalize.get_company_url) \
        == Signature(
            parameters=[
                Parameter(
                    name='company_id',
                    kind=Parameter.POSITIONAL_OR_KEYWORD,
                    default=Parameter.empty,
                    annotation=int,
                ),
            ],
            return_annotation=str,
    )


def test_module_attribute_signature() -> None:
    r"""Ensure module attributes' signature."""
    assert hasattr(news.crawlers.util.normalize, 'COMPANY_ID_LOOKUP_TABLE')
    assert news.crawlers.util.normalize.COMPANY_ID_LOOKUP_TABLE == {
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
    assert hasattr(news.crawlers.util.normalize, 'COMPANY_URL_LOOKUP_TABLE')
    assert news.crawlers.util.normalize.COMPANY_URL_LOOKUP_TABLE == {
        0: r'https://www.chinatimes.com/',
        1: r'https://www.cna.com.tw/news/aipl/',
        2: r'https://www.epochtimes.com/b5/',
        3: r'https://star.ettoday.net/news/',
        4: r'https://www.ftvnews.com.tw/news/detail/',
        5: r'https://news.ltn.com.tw/ajax/breakingnews/',
        6: r'https://www.ntdtv.com/b5/',
        7: r'https://www.setn.com/',
        8: r'https://www.storm.mg/article/',
        9: r'https://news.tvbs.com.tw/',
        10: r'https://udn.com/',
    }
    assert hasattr(
        news.crawlers.util.normalize,
        'COMPANY_URL_FASTEST_LOOKUP_TABLE',
    )
    assert news.crawlers.util.normalize.COMPANY_URL_FASTEST_LOOKUP_TABLE == [
        r'https://www.chinatimes.com/',
        r'https://www.cna.com.tw/news/aipl/',
        r'https://www.epochtimes.com/b5/',
        r'https://star.ettoday.net/news/',
        r'https://www.ftvnews.com.tw/news/detail/',
        r'https://news.ltn.com.tw/ajax/breakingnews/',
        r'https://www.ntdtv.com/b5/',
        r'https://www.setn.com/',
        r'https://www.storm.mg/article/',
        r'https://news.tvbs.com.tw/',
        r'https://udn.com/',
    ]
    assert hasattr(
        news.crawlers.util.normalize,
        'COMPRESS_URL_PATTERN_LOOKUP_TABLE',
    )
    assert news.crawlers.util.normalize.COMPRESS_URL_PATTERN_LOOKUP_TABLE == {
        0:
            re.compile(
                r'https://www.chinatimes.com/([rn])'
                + r'(?:ealtimenews|ewspapers)/(\d+)-(\d+)',
            ),
        1:
            re.compile(
                r'https://www.cna.com.tw/news/aipl/(\d+)\.aspx',
            ),
        2:
            re.compile(
                r'https://www.epochtimes.com/b5/(\d+)/(\d+)/(\d+)/n(\d+)\.htm',
            ),
        3:
            re.compile(
                r'https://star.ettoday.net/news/(\d+)',
            ),
        4:
            re.compile(
                r'https://www.ftvnews.com.tw/news/detail/(.+)',
            ),
        5:
            re.compile(
                r'https://news.ltn.com.tw/news/(\w+)/breakingnews/(\d+)',
            ),
        6:
            re.compile(
                r'https://www.ntdtv.com/b5/(\d+)/(\d+)/(\d+)/a(\d+)\.html',
            ),
        7:
            re.compile(
                r'https://www.setn.com/News.aspx\?.*NewsID=(\d+)',
            ),
        8:
            re.compile(
                r'https://www.storm.mg/article/(\d+)\?mode=whole',
            ),
        9:
            re.compile(
                r'https://news.tvbs.com.tw/(\w+)/(\d+)',
            ),
        10:
            re.compile(
                r'https://udn.com/news/story/(\d+)/(\d+)',
            ),
    }
    assert hasattr(
        news.crawlers.util.normalize,
        'COMPRESS_URL_PATTERN_FASTEST_LOOKUP_TABLE',
    )
    assert (
        news.crawlers.util.normalize.COMPRESS_URL_PATTERN_FASTEST_LOOKUP_TABLE
        == [
            re.compile(
                r'https://www.chinatimes.com/([rn])'
                + r'(?:ealtimenews|ewspapers)/(\d+)-(\d+)',
            ),
            re.compile(
                r'https://www.cna.com.tw/news/aipl/(\d+)\.aspx',
            ),
            re.compile(
                r'https://www.epochtimes.com/b5/(\d+)/(\d+)/(\d+)/n(\d+)\.htm',
            ),
            re.compile(
                r'https://star.ettoday.net/news/(\d+)',
            ),
            re.compile(
                r'https://www.ftvnews.com.tw/news/detail/(.+)',
            ),
            re.compile(
                r'https://news.ltn.com.tw/news/(\w+)/breakingnews/(\d+)',
            ),
            re.compile(
                r'https://www.ntdtv.com/b5/(\d+)/(\d+)/(\d+)/a(\d+)\.html',
            ),
            re.compile(
                r'https://www.setn.com/News.aspx\?.*NewsID=(\d+)',
            ),
            re.compile(
                r'https://www.storm.mg/article/(\d+)\?mode=whole',
            ),
            re.compile(
                r'https://news.tvbs.com.tw/(\w+)/(\d+)',
            ),
            re.compile(
                r'https://udn.com/news/story/(\d+)/(\d+)',
            ),
        ]
    )
    assert hasattr(news.crawlers.util.normalize, 'WHITESPACE_COLLAPSE_PATTERN')
    assert news.crawlers.util.normalize.WHITESPACE_COLLAPSE_PATTERN.pattern \
        == r'\s+'
