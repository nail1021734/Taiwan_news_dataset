import re
import unicodedata

import dateutil.parser
from bs4 import BeautifulSoup

from news.crawlers.db.schema import RawNews
from news.parse.db.schema import ParsedNews


REPORTER_PATTERN = re.compile(r'\(大紀元記者(.*?)報導\)')
URL_PATTERN = re.compile(
    r'/b5/(\d+)/(\d+)/(\d+)/n\d+\.htm'
)


def parse(ori_news: RawNews) -> ParsedNews:
    """Parse Epochtimes news from raw HTML.

    Input news must contain `raw_xml` and `url` since these
    information cannot be retrieved from `raw_xml`.
    """
    # Information which cannot be parsed.
    parsed_news = ParsedNews(
        url_pattern=ori_news.url_pattern,
        company_id=ori_news.company_id,
    )

    soup = None
    try:
        soup = BeautifulSoup(ori_news.raw_xml, 'html.parser')
    except Exception:
        raise ValueError('Invalid html format.')

    # News article.
    article = ''
    try:
        article_tags = soup.select('div#artbody > p,h2')
        article = ' '.join(map(lambda tag: tag.text.strip(), article_tags))
        article = unicodedata.normalize('NFKC', article).strip()
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
    news_datetime = ''
    try:
        match = URL_PATTERN.match(parsed_news.url_pattern)
        year = int(match.group(1))
        month = int(match.group(2))
        day = int(match.group(3))
        news_datetime = dateutil.parser.isoparse(
            f"20{year:02d}-{month:02d}-{day:02d}T00:00:00Z"
        )
        news_datetime = news_datetime.timestamp()
    except Exception:
        # There may not have category.
        news_datetime = ''

    # News reporter.
    reporter = ''
    try:
        reporter = REPORTER_PATTERN.search(article).group(1)
    except Exception:
        # There may not have reporter.
        reporter = ''

    # News title.
    title = ''
    try:
        title = soup.select('h1.title')[0].text
        title = unicodedata.normalize('NFKC', title).strip()
    except Exception:
        raise ValueError('Fail to parse epochtimes news title.')

    parsed_news.article = article
    parsed_news.category = category
    parsed_news.datetime = news_datetime
    parsed_news.reporter = reporter
    parsed_news.title = title
    return parsed_news
