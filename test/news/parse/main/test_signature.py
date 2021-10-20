import argparse
import inspect
from inspect import Parameter, Signature
from typing import Final, List

import news.parse.chinatimes
import news.parse.cna
import news.parse.epochtimes
import news.parse.ettoday
import news.parse.ftv
import news.parse.ltn
import news.parse.main
import news.parse.ntdtv
import news.parse.setn
import news.parse.storm
import news.parse.tvbs
import news.parse.udn


def test_module_function_signature() -> None:
    r"""Ensure module functions' signature."""
    assert hasattr(news.parse.main, 'parse_args')
    assert inspect.isfunction(news.parse.main.parse_args)
    assert (
        inspect.signature(news.parse.main.parse_args) == Signature(
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
    )
    assert hasattr(news.parse.main, 'parse_raw_news')
    assert inspect.isfunction(news.parse.main.parse_raw_news)
    assert (
        inspect.signature(news.parse.main.parse_raw_news) == Signature(
            parameters=[
                Parameter(
                    name='db_path',
                    kind=Parameter.POSITIONAL_OR_KEYWORD,
                    default=Parameter.empty,
                    annotation=Final[str],
                ),
                Parameter(
                    name='raw_news_list',
                    kind=Parameter.POSITIONAL_OR_KEYWORD,
                    default=Parameter.empty,
                    annotation=Final[List[news.crawlers.db.schema.RawNews]],
                ),
            ],
            return_annotation=List[news.parse.db.schema.ParsedNews],
        )
    )
    assert hasattr(news.parse.main, 'main')
    assert inspect.isfunction(news.parse.main.main)
    assert (
        inspect.signature(news.parse.main.main) == Signature(
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
    )


def test_module_attribute_signature() -> None:
    r"""Ensure module attributes' signature."""
    assert hasattr(news.parse.main, 'PARSER_LOOKUP_TABLE')
    assert news.parse.main.PARSER_LOOKUP_TABLE == {
        0: news.parse.chinatimes.parser,
        1: news.parse.cna.parser,
        2: news.parse.epochtimes.parser,
        3: news.parse.ettoday.parser,
        4: news.parse.ftv.parser,
        5: news.parse.ltn.parser,
        6: news.parse.ntdtv.parser,
        7: news.parse.setn.parser,
        8: news.parse.storm.parser,
        9: news.parse.tvbs.parser,
        10: news.parse.udn.parser,
    }
    assert hasattr(news.parse.main, 'PARSER_FASTEST_LOOKUP_TABLE')
    assert news.parse.main.PARSER_FASTEST_LOOKUP_TABLE == [
        news.parse.chinatimes.parser,
        news.parse.cna.parser,
        news.parse.epochtimes.parser,
        news.parse.ettoday.parser,
        news.parse.ftv.parser,
        news.parse.ltn.parser,
        news.parse.ntdtv.parser,
        news.parse.setn.parser,
        news.parse.storm.parser,
        news.parse.tvbs.parser,
        news.parse.udn.parser,
    ]
