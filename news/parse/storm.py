import re
from datetime import datetime, timedelta
from typing import List, Tuple

from bs4 import BeautifulSoup

import news.parse.util.normalize
from news.crawlers.db.schema import RawNews
from news.parse.db.schema import ParsedNews

ARTICLE_DECOMPOSE_LIST: str = re.sub(
    r'\s+',
    ' ',
    '''
    article > div#CMS_wrapper > blockquote,
    article > div#CMS_wrapper .related_copy_content,
    article > div#CMS_wrapper > p[aid] > .typeform-share link
    ''',
)

# second rule is for: 4031507
ARTICLE_SELECTOR_LIST: str = re.sub(
    r'\s+',
    ' ',
    '''
    div#article_inner_wrapper > article > div#CMS_wrapper p[aid],
    div#article_inner_wrapper > article > div#CMS_wrapper p[dir]
    ''',
)

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
        ''
    ),
    # Remove the editor information. This observation is made with `url_pattern
    # = 4028800`.
    (
        re.compile(r'\s*(?:責任|採訪|編輯|後製|撰稿)?(?:採訪|編輯|後製|撰稿)[:/]\w*'),
        '',
    ),
    # Remove the image source. This observation is made with `url_pattern
    # = 21314`.
    (
        re.compile(r'\(圖片來源:[^\)]*\)'),
        '',
    ),
    # Remove the url. This observation is made with `url_pattern = 21336`.
    (
        re.compile(r'研究報告網址:https?:\/\/[\da-z\.-_\/]+'),
        '',
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

    parsed_news.article = article
    parsed_news.category = category
    parsed_news.reporter = reporter
    parsed_news.timestamp = timestamp
    parsed_news.title = title
    return parsed_news
