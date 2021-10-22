import re
from datetime import datetime
from typing import Final, List, Tuple

from bs4 import BeautifulSoup

import news.parse.util.normalize
from news.crawlers.db.schema import RawNews
from news.parse.db.schema import ParsedNews

###############################################################################
#                                 WARNING:
# Patterns MUST remain unordered, in other words, the order of execution
# WILL NOT and MUST NOT effect the parsing results.
###############################################################################
REPORTER_PATTERNS: Final[List[re.Pattern]] = [
    # This observation is made with `url_pattern = 202110200353, 201501010021`.
    re.compile(r'\(中央社記者([^()]*?)\d+?日專?電\)'),
    # This observation is made with `url_pattern = 201501010071, 201501010087`.
    re.compile(r'\(中央社(?:記者)?([^()]*?)特稿\)'),
    # This observation is made with `url_pattern = 201501010002, 201412310239`.
    re.compile(r'\(中央社([^()]*?)\d+?日電?\)'),
    # This observation is made with `url_pattern = 201412300008, 201412300122`.
    re.compile(r'\(中央社([^()]*?)\d+?日綜合(?:外電)?(?:報導)?\)'),
    # This observation is made with `url_pattern = 201501010257, 201412300220`.
    re.compile(r'\(中央社([^()]*?)\d+?日[^()]*?電\)'),
]
ARTICLE_SUB_PATTERNS: Final[List[Tuple[re.Pattern, str]]] = [
    (
        re.compile(r'(\(編輯.*?\))'),
        '',
    ),
    (
        re.compile(r'(\(譯者.*?\))'),
        '',
    ),
    # Remove datetime strings at the end of article. This observation is made
    # with `url_pattern = 201501010002`.
    (
        re.compile(r'(\d+)$'),
        '',
    ),
    # Remove datetime strings at the end of paragraph. This observation is made
    # with `url_pattern = 201501010002`.
    (
        re.compile(r'。(\d+) '),
        '。 ',
    ),
    # Remove update hints. This observation is made with
    # `url_pattern = 201412300008`.
    (
        re.compile(r'(\(即時更新\))'),
        '',
    ),
]
TITLE_SUB_PATTERNS: Final[List[Tuple[re.Pattern, str]]] = [
    # Remove update hints. This observation is made with
    # `url_pattern = 201412300008`.
    (
        re.compile(r'【更新】'),
        '',
    ),
    # Remove video hints. This observation is made with
    # `url_pattern = 201412280286`.
    (
        re.compile(r'【影片】'),
        '',
    ),
]


def parser(raw_news: Final[RawNews]) -> ParsedNews:
    """Parse CNA news from raw HTML.

    Input news must contain `raw_xml` and `url` since these
    information cannot be retrieved from `raw_xml`.
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
        additional_tag = soup.select_one('div.dictionary')
        if additional_tag:
            article = additional_tag.text

        # Only first `div.centralContent div.paragraph` contains news.  News
        # are splitted into paragraph by `p` tags, which happens to be the
        # direct children of `div.centralContent div.paragraph`.  This
        # observation is made with `url_pattern = 201501010002`.
        article += ' '.join(
            map(
                lambda tag: tag.text,
                soup.select(
                    'div.centralContent div:nth-child(1 of .paragraph) > p',
                )
            )
        )
        article = news.parse.util.normalize.NFKC(article)
    except Exception:
        raise ValueError('Fail to parse CNA news article.')

    ###########################################################################
    # Parsing news category.
    ###########################################################################
    category = ''
    try:
        # There are only two tags in the breadcrumb links
        # `div.centralContent > div.breadcrumb > a`.  Category is contained in
        # the second tag of the breadcrumb links.  This
        # observation is made with `url_pattern = 201501010002`.
        category = soup.select('div.breadcrumb > a')[1].text
        category = news.parse.util.normalize.NFKC(category)
    except Exception:
        # There may not have category.
        category = ''

    ###########################################################################
    # Parsing news datetime.
    ###########################################################################
    news_datetime = 0
    try:
        # Some news publishing date time are different to URL pattern.  For
        # simplicity we only use URL pattern to represent the same news.  News
        # datetime will convert to POSIX time (which is under UTC time zone).
        news_datetime = int(
            datetime.strptime(
                parsed_news.url_pattern[:8],
                '%Y%m%d',
            ).timestamp()
        )
    except Exception:
        ValueError('Fail to parse CNA news datetime.')

    ###########################################################################
    # Parsing news reporter.
    ###########################################################################
    reporter_list = []
    reporter = ''
    try:
        for reporter_pattern in REPORTER_PATTERNS:
            # There might have more than one pattern matched.
            reporter_list.extend(reporter_pattern.findall(article))
            # Remove reporter text from article.
            article = news.parse.util.normalize.NFKC(
                reporter_pattern.sub('', article)
            )

        # Reporters are comma seperated.
        reporter = ','.join(reporter_list)
    except Exception:
        # There may not have reporter.
        reporter = ''

    ###########################################################################
    # Parsing news title.
    ###########################################################################
    title = ''
    try:
        # Title is in `div.centralContent h1 span`. This observation is made
        # with `url_pattern = 201501010002`.
        title = soup.select_one('div.centralContent h1 span').text
        title = news.parse.util.normalize.NFKC(title)
    except Exception:
        raise ValueError('Fail to parse CNA news title.')

    ###########################################################################
    # Remove bad article pattern.
    ###########################################################################
    try:
        for pttn, sub_str in ARTICLE_SUB_PATTERNS:
            article = news.parse.util.normalize.NFKC(
                pttn.sub(
                    sub_str,
                    article,
                )
            )
    except Exception:
        raise ValueError('Fail to substitude article pattern.')

    ###########################################################################
    # Remove bad title pattern.
    ###########################################################################
    try:
        for pttn, sub_str in TITLE_SUB_PATTERNS:
            title = news.parse.util.normalize.NFKC(pttn.sub(
                sub_str,
                title,
            ))
    except Exception:
        raise ValueError('Fail to substitude title pattern.')

    parsed_news.article = article
    if category:
        parsed_news.category = category
    else:
        parsed_news.category = ParsedNews.category
    parsed_news.datetime = news_datetime
    if reporter:
        parsed_news.reporter = reporter
    else:
        parsed_news.reporter = ParsedNews.reporter
    parsed_news.title = title
    return parsed_news
