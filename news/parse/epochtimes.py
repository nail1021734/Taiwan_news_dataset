import re
import unicodedata
from typing import Final

import dateutil.parser
from bs4 import BeautifulSoup

from news.crawlers.db.schema import RawNews
from news.parse.db.schema import ParsedNews

BAD_TITLE_PATTERNS = [
    re.compile(r'【.*?】'),
]
BAD_ARTICLE_PATTERNS = [
    re.compile(r'@\*#'),
    re.compile(r'\(轉自(.*?)/.*?\)'),
    re.compile(r'─+點閱\s*【.*?】\s*─+'),
    re.compile(r'點閱\s*【.*?】\s*系列文章'),
    re.compile(r'本文網址:\s*.*?$'),
    re.compile(r'【.*?】'),
    re.compile(r'責任編輯:.*$'),
]
REPORTER_PATTERNS = [
    re.compile(r'\(大紀元記者(.*?)報導\)'),
]
URL_PATTERN = re.compile(r'/b5/(\d+)/(\d+)/(\d+)/n\d+\.htm')


def parser(raw_news: Final[RawNews]) -> ParsedNews:
    """Parse Epochtimes news from raw HTML.

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

    # News article.
    article = ''
    try:
        article_tags = soup.select('div#artbody > p,h2')
        article = ' '.join(map(lambda tag: tag.text.strip(), article_tags))
        article = unicodedata.normalize('NFKC', article).strip()
        for pattern in BAD_ARTICLE_PATTERNS:
            article = pattern.sub('', article).strip()
    except Exception:
        raise ValueError('Fail to parse epochtimes news article.')

    # News category.
    category = ''
    try:
        category = soup.select('div#breadcrumb > a')[-1].text
        category = unicodedata.normalize('NFKC', category).strip()
    except Exception:
        # There may not have category.
        category = ''

    # News datetime.
    timestamp = ''
    try:
        match = URL_PATTERN.match(parsed_news.url_pattern)
        year = int(match.group(1))
        month = int(match.group(2))
        day = int(match.group(3))
        timestamp = dateutil.parser.isoparse(
            f"20{year:02d}-{month:02d}-{day:02d}T00:00:00Z"
        )
        timestamp = timestamp.timestamp()
    except Exception:
        # There may not have category.
        timestamp = ''

    # News reporter.
    reporter = ''
    try:
        for reporter_pattern in REPORTER_PATTERNS:
            search_result = reporter_pattern.search(article)
            if not search_result:
                continue
            article = article[search_result.end():]
            reporter = search_result.group(1)
    except Exception:
        # There may not have reporter.
        reporter = ''

    # News title.
    title = ''
    try:
        title = soup.select('h1.title')[0].text
        title = unicodedata.normalize('NFKC', title).strip()
        for pattern in BAD_TITLE_PATTERNS:
            title = pattern.sub('', title)
    except Exception:
        raise ValueError('Fail to parse epochtimes news title.')

    parsed_news.article = article
    parsed_news.category = category
    parsed_news.reporter = reporter
    parsed_news.timestamp = timestamp
    parsed_news.title = title
    return parsed_news
