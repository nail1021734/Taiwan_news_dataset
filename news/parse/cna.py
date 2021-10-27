import re
from datetime import datetime
from typing import Final, List, Tuple

from bs4 import BeautifulSoup

import news.parse.util.normalize
from news.crawlers.db.schema import RawNews
from news.parse.db.schema import ParsedNews

###############################################################################
#                                 WARNING:
# Patterns (including `REPORTER_PATTERNS`, `ARTICLE_SUB_PATTERNS`,
# `TITLE_SUB_PATTERNS`) MUST remain their relative ordered, in other words,
# the order of execution may effect the parsing results. `REPORTER_PATTERNS`
# MUST have exactly ONE group.  You can use `(?...)` pattern as non-capture
# group, see python's re module for details.
###############################################################################
REPORTER_PATTERNS: Final[List[re.Pattern]] = [
    # This observation is made with `url_pattern = 201411080177, 201411100007,
    # 201411100229, 201411100306, 201411100454, 201412030042, 201412260115,
    # 201412300008, 201412300122, 201412310239, 201501010002, 201501010021,
    # 201501010071, 201501010087, 201801010009, 201801010165, 201801040371,
    # 201801240404, 201806280284, 201807110318, 201808210054, 201812310105,
    # 201903240113, 201908030093, 201909290214, 201912070131, 202110200353`.
    re.compile(
        r'\(中?央社?(?:記者|網站)?\d*?日?([^)0-9]*?)'
        + r'\d*?\s*?年?\d*?\s*?月?\d*\s*?日?\d*?'
        + r'(?:綜合?)?(?:外|專)?(?:電|家)?(?:連線|更新)?(?:特稿|報導)?\)',
    ),
    # Must match '日' in the middle of text. This observation is made with
    # `url_pattern = 201911100105, 201501010257, 201412300220`.
    re.compile(
        r'\(\s 中?央社?(?:記者|網站)?\d*?日?([^)0-9]*?)'
        + r'\d*?年?\d*?月?\d*\s*?日?\d*?(?:日[^\)]*?)'
        + r'(?:綜合?)?(?:外|專)?(?:電|家)?(?:連線|更新)?(?:特稿|報導)?\)',
    ),
    # This observation is made with `url_pattern = 201807110178`.
    re.compile(r'中?央社?駐.*?特派員(.*?)/\d*?年?\d+?月?\d+?日'),
]
ARTICLE_SUB_PATTERNS: Final[List[Tuple[re.Pattern, str]]] = [
    # This observation is made with `url_pattern = 201901010005`.
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
        re.compile(r'\d+$'),
        '',
    ),
    # Remove datetime strings at the end of paragraph. This observation is made
    # with `url_pattern = 201412300008`.
    (
        re.compile(r'。\d+ '),
        '。 ',
    ),
    # Remove datetime strings at the end of paragraph. This observation is made
    # with `url_pattern = 201411090003`.
    (
        re.compile(r'」\d+ '),
        '」 ',
    ),
    # Remove update hints. This observation is made with
    # `url_pattern = 201412300008, 201411090158`.
    (
        re.compile(r'\((?:賽況)?(?:即時)?更新\)'),
        '',
    ),
    # Remove update hints. This observation is made with
    # `url_pattern = 201612180139, 201612070380`.
    (
        re.compile(r'(【[^】]*?】|\[[^\]]*?\])'),
        '',
    ),
    # Remove meaningless symbols. This observation is made with
    # `url_pattern = 201412040065`.
    (
        re.compile(r'★'),
        '',
    ),
    # Remove recommendations. This observation is made with `url_pattern =
    # 201412030008`.
    (
        re.compile(r'※你可能還想看:.*'),
        '',
    ),
    # Remove link. This observation is made with `url_pattern =
    # 201701010131`.
    (
        re.compile(r'。\s?\S*?連結點這裡'),
        '。',
    ),
    # Remove url. This observation is made with `url_pattern =
    # 201911110278`.
    (
        re.compile(r'([,。]募資連結https?:\/\/[\da-z\.-_\/]+)'),
        '',
    ),
    # Remove special column. This observation is made with `url_pattern =
    # 201810030025, 201612260025`.
    (
        re.compile(r'^\(?特派員[^\s。,]*?專欄\)?'),
        '',
    ),
    # Remove special column. This observation is made with `url_pattern =
    # 201910250015`.
    (
        re.compile(r'\(?延伸閱讀:?.*?\)?\s'),
        '',
    ),
    # Remove prefix. This observation is made with `url_pattern =
    # 201609300395, 201609300396, 201609300393, 201603130226, 201603130227`.
    (
        re.compile(r'^[^\s。,]*?專題(?:之[一二三四五六七八九十]+)?(?:\(\d+\))?'),
        '',
    ),
]
TITLE_SUB_PATTERNS: Final[List[Tuple[re.Pattern, str]]] = [
    # Remove content hints. This observation is made with
    # `url_pattern = 201412280286, 201412300008, 201701010135, 201801190132,
    # 201802070327, 201803060174, 201901010005, 201901010013, 202001010027,
    # 201910250015, 201911080011, 201912310042`.
    (
        re.compile(r'(【[^】]*?】|\[[^\]]*?\])'),
        '',
    ),
    # Remove meaningless symbols. This observation is made with
    # `url_pattern = 201412260020`.
    (
        re.compile(r'★'),
        '',
    ),
    # Remove article labels. This observation is made with
    # `url_pattern = 201612260025`.
    (
        re.compile(r'\s?特派專欄\s?'),
        '',
    ),
]


def parser(raw_news: Final[RawNews]) -> ParsedNews:
    """Parse CNA news from raw HTML.

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
        raise ValueError('Fail to parse CNA news datetime.')

    ###########################################################################
    # Parsing news reporter.
    ###########################################################################
    reporter_list = []
    reporter = ''
    try:
        for reporter_pttn in REPORTER_PATTERNS:
            # There might have more than one pattern matched.
            reporter_list.extend(reporter_pttn.findall(article))
            # Remove reporter text from article.
            article = news.parse.util.normalize.NFKC(
                reporter_pttn.sub('', article)
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
        raise ValueError('Fail to substitude CNA article pattern.')

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
        raise ValueError('Fail to substitude CNA title pattern.')

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
