import inspect
import re
from inspect import Parameter, Signature
from typing import Final

import news.crawlers.db.schema
import news.parse.ntdtv
import news.parse.db.schema
import news.parse.util.normalize


def test_module_function_signature() -> None:
    r"""Ensure module functions' signature."""
    assert hasattr(news.parse.ntdtv, 'parser')
    assert inspect.isfunction(news.parse.ntdtv.parser)
    assert inspect.signature(news.parse.ntdtv.parser) == Signature(
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
    assert hasattr(news.parse.ntdtv, 'ARTICLE_SELECTOR_LIST')
    assert news.parse.ntdtv.ARTICLE_SELECTOR_LIST == re.sub(
        r'\s+',
        ' ',
        '''
        div[itemprop=articleBody].post_content > p:not(:has(a:has(img))),
        div.article_content > p
        ''',
    )
    assert hasattr(news.parse.ntdtv, 'TITLE_SELECTOR_LIST')
    assert news.parse.ntdtv.TITLE_SELECTOR_LIST == re.sub(
        r'\s+',
        ' ',
        '''
        div.article_title > h1,
        div.main_title
        ''',
    )
    assert hasattr(news.parse.ntdtv, 'REPORTER_PATTERNS')
    assert news.parse.ntdtv.REPORTER_PATTERNS == [
        re.compile(
            r'\(?(?:(?:這|这)是)?新(?:唐|塘)人(?:記|记)?者?'
            + r'(?:亞太)?(?:(?:電|电)(?:視|视)(?:台|臺)?)?' + r'([\w、\s]*?)'
            + r'的?(?:(?:综|綜)合|整理|(?:採|采)(?:訪|访))?(?:報|报)(?:導|导|道)。?\)?'
        ),
        re.compile(r'文字:([^/]+?)/.+$'),
    ]
    assert hasattr(news.parse.ntdtv, 'ARTICLE_SUB_PATTERNS')
    assert news.parse.ntdtv.ARTICLE_SUB_PATTERNS == [
        (
            re.compile(r'\((攝影|圖片):[^)]+?\)'),
            '',
        ),
        (
            re.compile(r'@\*#'),
            '',
        ),
        (
            re.compile(r'[—–─]*\(?轉自[^)\s]*?\)?\s*(有(刪|删)(節|节))?$'),
            '',
        ),
        (
            re.compile(r'─+點閱\s*【.*?】\s*─+'),
            '',
        ),
        (
            re.compile(r'點閱\s*【.*?】\s*系列文章'),
            '',
        ),
        (
            re.compile(r'美東時間:\s*.*?【萬年曆】'),
            '',
        ),
        (
            re.compile(r'(本文|影片)網址為?:?\s*.*$'),
            '',
        ),
        (
            re.compile(r'^(【[^】]*?】)+'),
            '',
        ),
        (
            re.compile(r'【新(唐|塘)人[^】]*?訊】?'),
            '',
        ),
        (
            re.compile(r'【禁聞】\S+?\s?\S+?$'),
            '',
        ),
        (
            re.compile(r'待完成$'),
            '',
        ),
        (
            re.compile(r'相(關|关)((鏈|链)(接|結)|(視|视)(頻|频)|新(聞|闻))+?:.*$'),
            '',
        ),
        (
            re.compile(r'(撰文|(製|制)作):.*$'),
            ' ',
        ),
        (
            re.compile(r'訂閱\S+?:https://\S+?$'),
            '',
        ),
        (
            re.compile(
                r'\(?(大(紀|纪)元|中央社?)((記|记)者)?'
                + r'[^()0-9]*?\d*?[^()]*?((電|电)|(報|报)(導|导)|特稿|社)\)',
            ),
            '',
        ),
        (
            re.compile(r'\(((實|实)(習|习))?(編|编)?(譯|译)者?(:|;)[^)]+\)?'),
            '',
        ),
        (
            re.compile(r'\(本文附?(有|(帶|带))?((影音|(照|相)片)(及|和)?(帶|带)?)+\)'),
            '',
        ),
        (
            re.compile(r'\((自由亞洲電(臺|台)|美國之音)[^)]*?(报|報)導\)'),
            '',
        ),
        (
            re.compile(r'社(區|区)(廣|广)角(鏡|镜)\(\d+?\)(提要:)?'),
            '',
        ),
        (
            re.compile(r'新(聞|闻)(週|周)刊\(?\d+\)?期?'),
            '',
        ),
        (
            re.compile(r'\*(\S*?)\*'),
            r'\1',
        ),
        (
            re.compile(r'\s+(★|●|•)'),
            ' ',
        ),
        (
            re.compile(r'(\[(圖|图)卡\d*\]\s*|\((圖|图)片來源:.*?\))'),
            '',
        ),
        (
            re.compile(r'([^:])//'),
            r'\1',
        ),
        (
            re.compile(
                r'新(唐|塘)人(電|电)(視|视)(臺|台)\s*((https?://)?www\.ntdtv\.com)?',
            ),
            '',
        ),
        (
            re.compile(r'(下(載|载)(錄|录)像)'),
            '',
        ),
        (
            re.compile(r'\((畫|画)面.*?(報|报)(導|导|道)\)'),
            '',
        ),
        (
            re.compile(r'^(主播)?\)'),
            '',
        ),
        (
            re.compile(r'\s+相(關|关)新聞\s+'),
            ' ',
        ),
        (
            re.compile(r'\.html#video target=_blank>'),
            '',
        ),
        (
            re.compile(
                r'''[0-9a-zA-sÀ-ÿ,.:;?!&/“”’'"$%『』\[\]()*=—–─\-\s]+$''',
            ),
            '',
        ),
    ]
    assert hasattr(news.parse.ntdtv, 'TITLE_SUB_PATTERNS')
    assert news.parse.ntdtv.TITLE_SUB_PATTERNS == [
        (
            re.compile(r'(【[^】]*?】|\([^)]*?\))'),
            '',
        ),
        (
            re.compile(r'(快(訊|讯)|組(圖|图)|焦(點|点)人物):'),
            '',
        ),
        (
            re.compile(r'(—)+'),
            ' ',
        ),
    ]
