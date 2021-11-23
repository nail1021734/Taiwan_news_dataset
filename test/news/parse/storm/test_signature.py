import inspect
import re
from inspect import Parameter, Signature

import news.crawlers.db.schema
import news.parse.db.schema
import news.parse.storm
import news.parse.util.normalize


def test_module_function_signature() -> None:
    r"""Ensure module functions' signature."""
    assert hasattr(news.parse.storm, 'parser')
    assert inspect.isfunction(news.parse.storm.parser)
    assert inspect.signature(news.parse.storm.parser) == Signature(
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
    assert hasattr(news.parse.storm, 'ARTICLE_DECOMPOSE_LIST')
    assert news.parse.storm.ARTICLE_DECOMPOSE_LIST == re.sub(
        r'\s+',
        ' ',
        '''
        div#CMS_wrapper > blockquote,
        div#CMS_wrapper .related_copy_content,
        div#CMS_wrapper > p[aid] > .typeform-share link
        ''',
    )
    assert hasattr(news.parse.storm, 'ARTICLE_SELECTOR_LIST')
    assert news.parse.storm.ARTICLE_SELECTOR_LIST == re.sub(
        r'\s+',
        ' ',
        '''
        div#CMS_wrapper p[aid],
        div#CMS_wrapper p[dir]
        ''',
    )
    assert hasattr(news.parse.storm, 'TITLE_SELECTOR_LIST')
    assert news.parse.storm.TITLE_SELECTOR_LIST == re.sub(
        r'\s+',
        ' ',
        '''
        h1#article_title
        ''',
    )
    assert hasattr(news.parse.storm, 'ARTICLE_SUB_PATTERNS')
    assert news.parse.storm.ARTICLE_SUB_PATTERNS == [
        (
            re.compile(r'\*?作者(?:為|:)?[\s\w]*?$'),
            '',
        ),
        (
            re.compile(r'\s*(?:責任|採訪|編輯|後製|撰稿)?(?:採訪|編輯|後製|撰稿)[:/]\w*'),
            '',
        ),
        (
            re.compile(r'\(?(?:資料|圖片)來源:[^\)]*\)?'),
            '',
        ),
        (
            re.compile(
                r'(?:《刺胳針》|研究|探險隊遠征)?(?:報告|直播)?(?:網址|網站)?[\s:]*?'
                + r'https?:\/\/[\(\)%\da-z\.-_\/-]+'
            ),
            '',
        ),
        (
            re.compile(r'\d*?年?\d*?月?\d*?日?\s*?\w*?/綜合報導'),
            '',
        ),
        (
            re.compile(
                r'(?:【前言】|-{4,}\s*|原文、圖經授權轉載自BBC中文網|報名網址\s*?\(\S*?\)|'
                + r'(?:更多精彩內容|文/\S*?|加入風運動|歡迎上官網|【立即購票】|'
                + r'本文經授權轉載自|[➤◎*]).*?$)'
            ),
            '',
        ),
    ]
    assert hasattr(news.parse.storm, 'TITLE_SUB_PATTERNS')
    assert news.parse.storm.TITLE_SUB_PATTERNS == [
        (
            re.compile(
                r'([\(【](?:\d*?分?之\d*?|上|下|腦力犯中|下班經濟學)[\)】]|'
                + r'選摘\s*?\(\d*\)|^[\S\s]{,5}》)'
            ),
            '',
        ),
        (
            re.compile(r'\|'),
            ' ',
        ),
    ]
