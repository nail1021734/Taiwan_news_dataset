import inspect
import re
from inspect import Parameter, Signature

import news.crawlers.db.schema
import news.parse.db.schema
import news.parse.ntdtv
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
                annotation=news.crawlers.db.schema.RawNews,
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
            r'\(?(?:[這这]是)?新[唐塘]人[記记]?者?(?:亞太)?(?:[電电][視视][台臺]?)?'
            + r'([\w、\s]*?)的?(?:[综綜]合|整理|[採采][訪访])?[報报][導导道]。?\)?'
        ),
        re.compile(r'文字:([^/]+?)/.+$'),
    ]
    assert hasattr(news.parse.ntdtv, 'ARTICLE_SUB_PATTERNS')
    assert news.parse.ntdtv.ARTICLE_SUB_PATTERNS == [
        (
            re.compile(r'\(([攝摄]影|[圖图]片):[^)]+?\)'),
            '',
        ),
        (
            re.compile(r'@\*#'),
            '',
        ),
        (
            re.compile(r'[—–─]*\(?轉自[^)\s]*?\)?\s*(有[刪删][節节])?$'),
            '',
        ),
        (
            re.compile(r'─+[點点][閱阅]\s*【.*?】\s*─+'),
            '',
        ),
        (
            re.compile(r'[點点][閱阅]\s*【.*?】\s*系列文章'),
            '',
        ),
        (
            re.compile(r'美[東东][時时][间間]:\s*.*?【[萬万]年[曆历]】'),
            '',
        ),
        (
            re.compile(r'(本文|影片)[網网]址[為为]?:?\s*.*$'),
            '',
        ),
        (
            re.compile(r'^(【[^】]*?】)+'),
            '',
        ),
        (
            re.compile(r'【新[唐塘]人[^】]*?[訊讯]】?'),
            '',
        ),
        (
            re.compile(r'【禁[聞闻]】\S+?\s?\S+?$'),
            '',
        ),
        (
            re.compile(r'待完成$'),
            '',
        ),
        (
            re.compile(r'相[關关]([鏈链][接結]|[視视][頻频]|新[聞闻])+?:.*$'),
            '',
        ),
        (
            re.compile(r'(撰文|[製制]作):.*$'),
            ' ',
        ),
        (
            re.compile(r'[訂订][閱阅]\S+?:https://\S+?$'),
            '',
        ),
        (
            re.compile(
                r'\(?(大[紀纪]元|中央社?)([記记]者)?'
                + r'[^()0-9]*?\d*?[^()]*?([電电]|[報报][導导道]|特稿|社)\)',
            ),
            '',
        ),
        (
            re.compile(r'\(([實实][習习])?[編编]?[譯译]者?(:|;)[^)]+\)?'),
            '',
        ),
        (
            re.compile(r'\(本文[附有帶带影音照相片及和]+\)'),
            '',
        ),
        (
            re.compile(r'\((自由亞洲電[臺台]|美國之音)[^)]*?[报報][導导道]\)'),
            '',
        ),
        (
            re.compile(r'社[區区][廣广]角[鏡镜]\(\d+?\)(提要:)?'),
            '',
        ),
        (
            re.compile(r'新[聞闻][週周]刊\(?\d+\)?期?'),
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
            re.compile(r'(\[[圖图]卡\d*\]\s*|\([圖图]片來源:.*?\))'),
            '',
        ),
        (
            re.compile(r'([^:])//'),
            r'\1',
        ),
        (
            re.compile(
                r'新[唐塘]人[電电][視视][臺台]\s*((https?://)?www\.ntdtv\.com)?',
            ),
            '',
        ),
        (
            re.compile(r'(下[載载][錄录]像)'),
            '',
        ),
        (
            re.compile(r'\([畫画]面.*?[報报][導导道]\)'),
            '',
        ),
        (
            re.compile(r'^(主播)?\)'),
            '',
        ),
        (
            re.compile(r'\s+相[關关]新聞\s+'),
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
            re.compile(r'(快[訊讯]|組[圖图]|焦[點点]人物):'),
            '',
        ),
        (
            re.compile(r'(—)+'),
            ' ',
        ),
    ]
