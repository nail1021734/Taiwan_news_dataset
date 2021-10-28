import inspect
import re
from inspect import Parameter, Signature

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
                annotation=news.crawlers.db.schema.RawNews,
            ),
        ],
        return_annotation=news.parse.db.schema.ParsedNews,
    )


def test_module_attribute_signature() -> None:
    r"""Ensure module attributes' signature."""
    assert hasattr(news.parse.cna, 'REPORTER_PATTERNS')
    assert news.parse.cna.REPORTER_PATTERNS == [
        re.compile(
            r'^\(中?央社?(?:記者|網站)?\d*?日?([^)0-9]*?)'
            + r'\d*?\s*?年?\d*?\s*?月?\d*\s*?日?\d*?'
            + r'(?:綜合?)?(?:外|專)?(?:電|家)?(?:連線|更新)?(?:特稿|報導)?\)',
        ),
        re.compile(
            r'\(\s?中?央社?(?:記者|網站)?\d*?日?([^)0-9]*?)'
            + r'\d*?年?\d*?月?\d*\s*?日?\d*?(?:日[^\)]*?)'
            + r'(?:綜合?)?(?:外|專)?(?:電|家)?(?:連線|更新)?(?:特稿|報導)?\)',
        ),
        re.compile(r'中?央社?駐.*?特派員(.*?)/\d*?年?\d+?月?\d+?日'),
    ]
    assert hasattr(news.parse.cna, 'ARTICLE_SUB_PATTERNS')
    assert news.parse.cna.ARTICLE_SUB_PATTERNS == [
        (
            re.compile(r'(\((實習)?(編?[輯譯]者?|核稿):?.*?\))'),
            '',
        ),
        (
            re.compile(r'\d+$'),
            '',
        ),
        (
            re.compile(r'。\d+ '),
            '。 ',
        ),
        (
            re.compile(r'」\d+ '),
            '」 ',
        ),
        (
            re.compile(r'\((?:賽況)?(?:即時)?更新\)'),
            '',
        ),
        (
            re.compile(r'(【[^】]*?】|\[[^\]]*?\])'),
            '',
        ),
        (
            re.compile(r'●'),
            ' ',
        ),
        (
            re.compile(r'(?:★|\s*?\.$)'),
            '',
        ),
        (
            re.compile(r'※你可能還想看:.*'),
            '',
        ),
        (
            re.compile(r'。\s?\S*?連結點這裡'),
            '。',
        ),
        (
            re.compile(r'([,。]募資連結https?:\/\/[\da-z\.-_\/]+|請上「中央社好POD」.*。$)'),
            '',
        ),
        (
            re.compile(r'^\(?特派員[^\s。,]*?專欄\)?'),
            '',
        ),
        (
            re.compile(r'\(?延伸閱讀[^\)。,]*\)?(?=\s+?[^\s。,]*)'),
            '',
        ),
        (
            re.compile(r'^[^\s。,]*?專題(?:之[一二三四五六七八九十]+)?(?:\(\d+\))?'),
            '',
        ),
        (
            re.compile(r'\s▼.*?(。\s|$)'),
            '',
        ),
        (
            re.compile(r'(?:自殺警語:)?珍惜生命,自殺不能解決問題,生命一定可以找到出路.*$'),
            '',
        ),
        (
            re.compile(r'\(?飲酒過量有害(身體)?健康[,.。;]酒後勿開車[,.。;]未(成年|滿18歲)請勿飲酒\)?'),
            '',
        ),
        (
            re.compile(r'\s*吸菸有害(身體)?健康[,.。;]未(成年|滿18歲)請勿吸菸。$'),
            '',
        ),
    ]
    assert hasattr(news.parse.cna, 'TITLE_SUB_PATTERNS')
    assert news.parse.cna.TITLE_SUB_PATTERNS == [
        (
            re.compile(r'(【[^】]*?】|\[[^\]]*?\]|\s*?特派專欄\s*?)'),
            '',
        ),
        (
            re.compile(r'★'),
            '',
        ),
    ]
