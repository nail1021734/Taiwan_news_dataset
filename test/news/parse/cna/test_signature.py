import inspect
import re
from datetime import datetime
from inspect import Parameter, Signature
from typing import Final

import news.crawlers.db.schema
import news.parse.cna
import news.parse.db.schema
import news.parse.util.normalize


def test_module_function_signature() -> None:
    r"""Ensure module functions' signature."""
    assert hasattr(news.parse.cna, 'parser')
    assert inspect.isfunction(news.parse.cna.parser)
    assert inspect.signature(news.parse.cna.parser) == Signature(
        parameters=[
            Parameter(
                name='raw_news',
                kind=Parameter.POSITIONAL_OR_KEYWORD,
                default=Parameter.empty,
                annotation=Final[news.crawlers.db.schema.RawNews],
            ),
        ],
        return_annotation=news.parse.db.schema.ParsedNews,
    )


def test_module_attribute_signature() -> None:
    r"""Ensure module attributes' signature."""
    assert hasattr(news.parse.cna, 'REPORTER_PATTERNS')
    assert news.parse.cna.REPORTER_PATTERNS == [
        re.compile(r'\(中央社(?:記者)([^()]*?)\d+?日專?電\)'),
        re.compile(r'\(中央社(?:記者)?([^()]*?)特稿\)'),
        re.compile(r'\(中央社(?:記者)([^()]*?)\d+?日?\d*?電?\)'),
        re.compile(r'\(中央社?([^()]*?)\d*?日綜合(?:外電)?(?:報導)?\)'),
        re.compile(r'\(中央社([^()]*?)\d+?日[^()]*?電\)'),
        re.compile(r'\(中央社([^()]*?)\d+?年\d+?月[^()]*?電\)'),
    ]
    assert hasattr(news.parse.cna, 'ARTICLE_SUB_PATTERNS')
    assert news.parse.cna.ARTICLE_SUB_PATTERNS == [
        (
            re.compile(r'(\(編輯.*?\))'),
            '',
        ),
        (
            re.compile(r'(\(譯者.*?\))'),
            '',
        ),
        (
            re.compile(r'(\d+)$'),
            '',
        ),
        (
            re.compile(r'。(\d+) '),
            '。 ',
        ),
        (
            re.compile(r'」\d+ '),
            '」 ',
        ),
        (
            re.compile(r'(\(即時更新\))'),
            '',
        ),
        (
            re.compile(r'★'),
            '',
        ),
        (
            re.compile(r'※你可能還想看:.*'),
            '',
        ),
    ]
    assert hasattr(news.parse.cna, 'TITLE_SUB_PATTERNS')
    assert news.parse.cna.TITLE_SUB_PATTERNS == [
        (
            re.compile(r'【更新】'),
            '',
        ),
        (
            re.compile(r'【影片】'),
            '',
        ),
        (
            re.compile(r'★'),
            '',
        ),
    ]
