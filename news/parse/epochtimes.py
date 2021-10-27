import re
from datetime import datetime
from typing import List, Tuple

from bs4 import BeautifulSoup

import news.parse.util.normalize
from news.crawlers.db.schema import RawNews
from news.parse.db.schema import ParsedNews

# News articles are located in `div#artbody`, and all of them are either `p` or
# `h2` tags.  `h2` tags represent section header and `p` tags represent normal
# paragprah.  Some `p` tags content figures and figure-captions which we do not
# need, thus we remove it with `p:not(:has(figure))`.
# This observation is made with `url_pattern = 21-10-27-13332627,
# 14-1-1-4048433`.
ARTICLE_SELECTOR_LIST: str = re.sub(
    r'\s+',
    ' ',
    '''
    div#artbody > :is(p:not(:has(figure)), h2)
    ''',
)

# News title is located in `h1.title`.
# This observation is made with `url_pattern = 21-10-27-13332627,
# 2011-04-12-517548`.
TITLE_SELECTOR_LIST: str = re.sub(
    r'\s+',
    ' ',
    '''
    h1.title
    ''',
)

###############################################################################
#                                 WARNING:
# Patterns (including `REPORTER_PATTERNS`, `ARTICLE_SUB_PATTERNS`,
# `TITLE_SUB_PATTERNS`) MUST remain their relative ordered, in other words,
# the order of execution may effect the parsing results. `REPORTER_PATTERNS`
# MUST have exactly ONE group.  You can use `(?...)` pattern as non-capture
# group, see python's re module for details.
###############################################################################
# This observation is made with `url_pattern = 14-1-1-4048455, 14-1-1-4048450,
# 13-12-31-4046950, 13-12-30-4046025`.
REPORTER_PATTERNS: List[re.Pattern] = [
    re.compile(
        r'\((?:[這这]是)?大[紀纪]元[記记]?者?(?:亞太)?(?:[電电][視视][台臺]?)?'
        + r'([\w、\s]*?)[的综綜合整理採采訪访編编譯译報报導导道]+?。?\)'
    ),
]
ARTICLE_SUB_PATTERNS: List[Tuple[re.Pattern, str]] = [
    (
        re.compile(r'@\*#'),
        '',
    ),
    # This observation is made with `url_pattern = 14-1-1-4048450,
    # 14-1-1-4047920`.
    (
        re.compile(
            r'\(?(新[唐塘]人|中央社?)([記记]者)?'
            + r'[^()0-9]*?\d*?[^()]*?([電电]|[報报][導导道]|特稿|社)\)',
        ),
        '',
    ),
    # This observation is made with `url_pattern = 14-1-1-4047920,
    # 13-12-31-4047555, 13-12-31-4047176, 13-12-31-4047058, 13-12-30-4046768,
    # 13-12-28-4044667`.
    (
        re.compile(
            r'\([據据]?(BBC(中文[網网])?|法[廣广]|自由亞洲電[臺台]|美國之音|[台民][視视])'
            + r'[^)]*?([報报][導导道])?\)',
        ),
        '',
    ),
    # This observation is made with `url_pattern = 14-1-1-4048382`.
    (
        re.compile(r'\(([實实][習习])?[編编]?[譯译]者?[:;][^)]+\)?'),
        '',
    ),
    # Note that `ord('–') == 8211`, `ord('—') == 8212` and `ord('─') == 9472`.
    (
        re.compile(r'[—–─]*\(?轉自[^)\s]*?\)?\s*(有[刪删][節节])?$'),
        '',
    ),
    # This observation is made with `url_pattern = 13-9-21-3969060`.
    (
        re.compile(r'\([^)]*?來稿\)'),
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
        re.compile(r'(本文|影片)網址為?:?\s*.*$'),
        '',
    ),
    (
        re.compile(r'^(【[^】]*?】)+'),
        '',
    ),
    # Remove useless symbols.
    # This observation is made with `url_pattern = 13-9-21-3969060`.
    (
        re.compile(r'◇'),
        '',
    ),
    # This observation is made with `url_pattern = 21-10-27-13332627,
    # 14-1-1-4048468, 14-1-1-4048456, 14-1-1-4047776`.
    (
        re.compile(r'\(?[責责]任?[編编][輯辑]?:.*$'),
        '',
    ),
]
TITLE_SUB_PATTERNS: List[Tuple[re.Pattern, str]] = [
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
URL_PATTERN = re.compile(r'/b5/(\d+)/(\d+)/(\d+)/n\d+\.htm')


def parser(raw_news: RawNews) -> ParsedNews:
    """Parse EPOCHTIMES news from raw HTML.

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
        article = ' '.join(
            map(lambda tag: tag.text, soup.select(ARTICLE_SELECTOR_LIST))
        )
        article = news.parse.util.normalize.NFKC(article)
    except Exception:
        raise ValueError('Fail to parse EPOCHTIMES news article.')

    ###########################################################################
    # Parsing news category.
    ###########################################################################
    category = ''
    try:
        # Sometimes news does not have categories, but if they do,  categories
        # are always located in breadcrumbs `div#breadcrumb > a`.
        # The first text in breadcrumb is always '首頁', so we exclude it.
        # The second text in breadcrumb is media type, we also exclude it.
        # There might be more than one category.  Thus we include them all and
        # save as comma separated format.  Some categories are duplicated, thus
        # we remove it using `list(dict.fromkeys(...))`.
        category = ','.join(
            list(
                dict.fromkeys(
                    map(
                        lambda tag: tag.text,
                        soup.select('div#breadcrumb > a')[2:],
                    )
                )
            )
        )
        category = news.parse.util.normalize.NFKC(category)
    except Exception:
        # There may not have category.
        category = ''

    ###########################################################################
    # Parsing news datetime.
    ###########################################################################
    timestamp = 0
    try:
        # Some news publishing date time are different to URL pattern.  For
        # simplicity we only use URL pattern to represent the same news.  News
        # datetime will convert to POSIX time (which is under UTC time zone).
        year, month, day, _ = parsed_news.url_pattern.split('-')
        year = f'20{year}'
        if len(month) == 1:
            month = f'0{month}'
        if len(day) == 1:
            day = f'0{day}'
        timestamp = int(
            datetime.strptime(f'{year}{month}{day}', '%Y%m%d').timestamp()
        )
    except Exception:
        raise ValueError('Fail to parse EPOCHTIMES news datetime.')

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
        reporter = ','.join(map(news.parse.util.normalize.NFKC, reporter_list))
        # Some reporters are separated by whitespaces or '、'.
        reporter = news.parse.util.normalize.NFKC(
            re.sub(
                r'[\s、]+',
                ',',
                reporter,
            )
        )
    except Exception:
        # There may not have reporter.
        reporter = ''

    ###########################################################################
    # Parsing news title.
    ###########################################################################
    title = ''
    try:
        title = soup.select_one(TITLE_SELECTOR_LIST).text
        title = news.parse.util.normalize.NFKC(title)
    except Exception:
        raise ValueError('Fail to parse EPOCHTIMES news title.')

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
        raise ValueError('Fail to substitude EPOCHTIMES article pattern.')

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
        raise ValueError('Fail to substitude EPOCHTIMES title pattern.')

    parsed_news.article = article
    if category:
        parsed_news.category = category
    else:
        parsed_news.category = ParsedNews.category
    if reporter:
        parsed_news.reporter = reporter
    else:
        parsed_news.reporter = ParsedNews.reporter
    parsed_news.timestamp = timestamp
    parsed_news.title = title
    return parsed_news
