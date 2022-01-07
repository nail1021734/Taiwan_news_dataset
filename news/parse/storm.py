import re
from datetime import datetime, timedelta
from typing import List, Tuple

from bs4 import BeautifulSoup

import news.parse.util.normalize
from news.crawlers.db.schema import RawNews
from news.parse.db.schema import ParsedNews

# Remove the following content:
# - Extra information about this article:
#   Paragraphs in `blockquote` tags are usually article supplementary
#   information.
#   This observation is made with `url_pattern  = 4029670, 4032502'.
ARTICLE_DECOMPOSE_LIST: str = re.sub(
    r'\s+',
    ' ',
    '''
    div#CMS_wrapper > blockquote,
    div#CMS_wrapper .related_copy_content,
    div#CMS_wrapper > p[aid] > .typeform-share link
    ''',
)

# News paragraphs are in the `div#CMS_wrapper p[aid]`.
# Select the `p` tags with a `aid` attribute. But there is a case that articles
# are wrapped in the `p[dir]` tag.
# This observation is made with `url_pattern = 4031507`.
ARTICLE_SELECTOR_LIST: str = re.sub(
    r'\s+',
    ' ',
    '''
    div#CMS_wrapper p[aid],
    div#CMS_wrapper p[dir]
    ''',
)

# Title is in `h1#article_title`.
# This observation is made with `url_pattern = 4031976`.
TITLE_SELECTOR_LIST: str = re.sub(
    r'\s+',
    ' ',
    '''
    h1#article_title
    ''',
)

ARTICLE_SUB_PATTERNS: List[Tuple[re.Pattern, str]] = [
    # Remove author information in the end of article. This observation is made
    # with `url_pattern = 4020745, 4029623`.
    (
        re.compile(r'\*?作者(?:為|:)?[\s\w]*?$'),
        '',
    ),
    # Remove the editor information. This observation is made with `url_pattern
    # = 4028800`.
    (
        re.compile(r'\s*(?:責任|採訪|編輯|後製|撰稿)?(?:採訪|編輯|後製|撰稿)[:/]\w*'),
        '',
    ),
    # Remove the source infomation. This observation is made with `url_pattern
    # = 21314, 26309`.
    (
        re.compile(r'\(?(?:資料|圖片)來源:[^\)]*\)?'),
        '',
    ),
    # Remove the url. This observation is made with `url_pattern = 21336,
    # 21679, 21680, 21747`.
    (
        re.compile(
            r'(?:《刺胳針》|研究|探險隊遠征)?(?:報告|直播)?(?:網址|網站)?[\s:]*?'
            + r'https?:\/\/[\(\)%\da-z\.-_\/-]+'
        ),
        '',
    ),
    # Remove the reporter. This observation is made with `url_pattern = 21680`.
    (
        re.compile(r'\d*?年?\d*?月?\d*?日?\s*?\w*?/綜合報導'),
        '',
    ),
    # Remove the extra information. This observation is made with
    # `url_pattern = 22241, 600064, 604069, 601210, 601348, 601417, 604783,
    # 604954, 612999, 620821`.
    (
        re.compile(
            r'(?:【前言】|-{4,}\s*|原文、圖經授權轉載自BBC中文網|報名網址\s*?\(\S*?\)|'
            + r'(?:更多精彩內容|文/\S*?|加入風運動|歡迎上官網|【立即購票】|' + r'本文經授權轉載自|[➤◎*]).*?$)'
        ),
        '',
    ),
]
TITLE_SUB_PATTERNS: List[Tuple[re.Pattern, str]] = [
    # Remove fraction information. This observation is made with `url_pattern
    # = 22241, 26950, 600064, 603975, 612999, 629038, 629129`.
    (
        re.compile(
            r'([\(【](?:\d*?分?之\d*?|上|下|腦力犯中|下班經濟學)[\)】]|'
            + r'選摘\s*?\(\d*\)|^[\S\s]{,5}》)'
        ),
        '',
    ),
    # Remove separation symbol. This observation is made with `url_pattern
    # = 601417`.
    (
        re.compile(r'\|'),
        ' ',
    ),
]


def parser(raw_news: RawNews) -> ParsedNews:
    """Parse STORM news from raw HTML.

    Input news must contain `raw_xml` and `url` since these information cannot
    be retrieved from `raw_xml`.
    """
    # Information which cannot be parsed from `raw_xml`.
    parsed_news = ParsedNews(
        url_pattern=raw_news.url_pattern,
        company_id=raw_news.company_id,
    )

    try:
        soup = BeautifulSoup(raw_news.raw_xml, 'html.parser')
    except Exception:
        raise ValueError('Invalid html format.')

    ###########################################################################
    # Parsing news article.
    ###########################################################################
    article = ''
    try:
        list(
            map(
                lambda tag: tag.decompose(),
                soup.select(ARTICLE_DECOMPOSE_LIST),
            )
        )
        # Next we retrieve tags contains article text.  This statement must
        # always put after tags removing statement.
        article += ' '.join(
            map(
                lambda tag: tag.text,
                soup.select(ARTICLE_SELECTOR_LIST),
            )
        )
        article = news.parse.util.normalize.NFKC(article)
    except Exception:
        raise ValueError('Fail to parse STORM news article.')

    ###########################################################################
    # Parsing news category.
    ###########################################################################
    category = ''
    try:
        # News category is always in the `div#title_tags_wrapper` tag. Since
        # there may be multiple `a` tags in the `title_tags_wrapper`, so we
        # use comma to concat them.
        category = news.parse.util.normalize.NFKC(
            ','.join(
                map(
                    lambda tag: tag.text,
                    soup.select('div#title_tags_wrapper a')
                )
            )
        )
    except Exception:
        # There may not have category.
        category = ''

    ###########################################################################
    # Parsing news datetime.
    ###########################################################################
    timestamp = 0
    try:
        # News publishing date and time is always in the `span#info_time` tag.
        # We will convert datetime to POSIX time which is under UTC time zone.
        timestamp = datetime.strptime(
            soup.select('span#info_time')[0].text,
            '%Y-%m-%d %H:%M',
        )
        # Convert to UTC.
        timestamp = timestamp - timedelta(hours=8)
        timestamp = int(timestamp.timestamp())
    except Exception:
        # There may not have category.
        timestamp = 0

    ###########################################################################
    # Parsing news reporter.
    ###########################################################################
    reporter = ''
    try:
        # News reporter is always in `div#author_block span.info_author` tag.
        # 有些新聞來自其他新聞網站, reporter tag 會直接顯示該新聞來源, 如來自中央社的新聞,
        # `reporter` == '中央社'.
        # This observation is made with `url_pattern = 4034287`.
        reporter = news.parse.util.normalize.NFKC(
            soup.select('div#author_block span.info_author')[0].text
        )
    except Exception:
        # There may not have reporter.
        reporter = ''

    ###########################################################################
    # Parsing news title.
    ###########################################################################
    title = ''
    try:
        title = ''.join(
            map(lambda tag: tag.text, soup.select(TITLE_SELECTOR_LIST))
        )
        title = news.parse.util.normalize.NFKC(title)
    except Exception:
        # storm response 404 with status code 200.
        # Thus some pages do not have title since it is 404.
        raise ValueError('Fail to parse STORM news title.')

    ###########################################################################
    # Substitude some article pattern.
    ###########################################################################
    try:
        for article_pttn, article_sub_str in ARTICLE_SUB_PATTERNS:
            article = news.parse.util.normalize.NFKC(
                article_pttn.sub(
                    article_sub_str,
                    article,
                )
            )
    except Exception:
        raise ValueError('Fail to substitude STORM article pattern.')

    ###########################################################################
    # Substitude some title pattern.
    ###########################################################################
    try:
        for title_pttn, title_sub_str in TITLE_SUB_PATTERNS:
            title = news.parse.util.normalize.NFKC(
                title_pttn.sub(
                    title_sub_str,
                    title,
                )
            )
    except Exception:
        raise ValueError('Fail to substitude STORM title pattern.')

    parsed_news.article = article
    parsed_news.category = category
    parsed_news.reporter = reporter
    parsed_news.timestamp = timestamp
    parsed_news.title = title
    return parsed_news
