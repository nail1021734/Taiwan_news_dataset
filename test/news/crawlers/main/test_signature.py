import argparse
import inspect
from inspect import Parameter, Signature
from typing import Final, List

import news.crawlers.chinatimes
import news.crawlers.cna
import news.crawlers.db.schema
import news.crawlers.epochtimes
import news.crawlers.ettoday
import news.crawlers.ftv
import news.crawlers.ltn
import news.crawlers.main
import news.crawlers.ntdtv
import news.crawlers.setn
import news.crawlers.storm
import news.crawlers.tvbs
import news.crawlers.udn


def test_module_function_signature() -> None:
    r"""Ensure module functions' signature."""
    assert hasattr(news.crawlers.main, 'parse_args')
    assert inspect.isfunction(news.crawlers.main.parse_args)
    assert inspect.signature(news.crawlers.main.parse_args) == Signature(
        parameters=[
            Parameter(
                name='argv',
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Parameter.empty,
                annotation=Final[List[str]],
            ),
        ],
        return_annotation=argparse.Namespace,
    )
    assert hasattr(news.crawlers.main, 'main')
    assert inspect.isfunction(news.crawlers.main.main)
    assert inspect.signature(news.crawlers.main.main) == Signature(
        parameters=[
            Parameter(
                name='argv',
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Parameter.empty,
                annotation=Final[List[str]],
            ),
        ],
        return_annotation=None,
    )


def test_module_attribute_signature() -> None:
    r"""Ensure module attributes' signature."""
    assert hasattr(news.crawlers.main, 'CRAWLER_SCRIPT_LOOKUP_TABLE')
    assert news.crawlers.main.CRAWLER_SCRIPT_LOOKUP_TABLE == {
        'chinatimes': news.crawlers.chinatimes.main,
        'cna': news.crawlers.cna.main,
        'epochtimes': news.crawlers.epochtimes.main,
        'ettoday': news.crawlers.ettoday.main,
        'ftv': news.crawlers.ftv.main,
        'ltn': news.crawlers.ltn.main,
        'ntdtv': news.crawlers.ntdtv.main,
        'setn': news.crawlers.setn.main,
        'storm': news.crawlers.storm.main,
        'tvbs': news.crawlers.tvbs.main,
        'udn': news.crawlers.udn.main,
    }
