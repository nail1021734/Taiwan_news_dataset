import inspect
import re
from datetime import datetime
from inspect import Parameter, Signature
from typing import Final

import news.crawlers.util.date_parse


def test_module_function_signature() -> None:
    r"""Ensure module functions' signature."""
    assert hasattr(news.crawlers.util.date_parse, 'epochtimes')
    assert inspect.isfunction(news.crawlers.util.date_parse.epochtimes)
    assert (
        inspect.signature(news.crawlers.util.date_parse.epochtimes)
        ==
        Signature(
            parameters=[
                Parameter(
                    name='url',
                    kind=Parameter.POSITIONAL_OR_KEYWORD,
                    default=Parameter.empty,
                    annotation=Final[str],
                ),
            ],
            return_annotation=datetime,
        )
    )
    assert hasattr(news.crawlers.util.date_parse, 'ntdtv')
    assert inspect.isfunction(news.crawlers.util.date_parse.ntdtv)
    assert (
        inspect.signature(news.crawlers.util.date_parse.ntdtv)
        ==
        Signature(
            parameters=[
                Parameter(
                    name='url',
                    kind=Parameter.POSITIONAL_OR_KEYWORD,
                    default=Parameter.empty,
                    annotation=Final[str],
                ),
            ],
            return_annotation=datetime,
        )
    )


def test_module_attribute_signature() -> None:
    r"""Ensure module attributes' signature."""
    assert hasattr(news.crawlers.util.date_parse, 'EPOCHTIMES_URL_PATTERN')
    assert isinstance(
        news.crawlers.util.date_parse.EPOCHTIMES_URL_PATTERN,
        re.Pattern,
    )
    assert (
        news.crawlers.util.date_parse.EPOCHTIMES_URL_PATTERN.pattern
        ==
        r'https://www.epochtimes.com/b5/(\d+)/(\d+)/(\d+)/n\d+\.htm'
    )
    assert hasattr(news.crawlers.util.date_parse, 'NTDTV_URL_PATTERN')
    assert isinstance(
        news.crawlers.util.date_parse.NTDTV_URL_PATTERN,
        re.Pattern,
    )
    assert (
        news.crawlers.util.date_parse.NTDTV_URL_PATTERN.pattern
        ==
        r'https://www.ntdtv.com/b5/(\d+)/(\d+)/(\d+)/a\d+.html'
    )
