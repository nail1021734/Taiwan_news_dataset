import re
import unicodedata
from datetime import datetime, timedelta

from bs4 import BeautifulSoup

from news.util.db.schema import News

REPORTER_PATTERN = re.compile(r'\((.*?)\)')


def parse(ori_news: News) -> News:
    """Parse CNA news from raw HTML.

    Input news must contain `raw_xml` and `url` since these
    information cannot be retrieved from `raw_xml`.
    """
    # Information which cannot be parsed.
    parsed_news = News(
        # Minimize `raw_xml`.
        raw_xml=re.sub(r'\s+', ' ', ori_news.raw_xml),
        url=ori_news.url,
    )

    soup = None
    try:
        soup = BeautifulSoup(parsed_news.raw_xml, 'html.parser')
    except Exception:
        raise ValueError('Invalid html format.')

    # News article.
    article = ''
    try:
        additional_tag = soup.select_one('div.dictionary')
        if additional_tag:
            article = additional_tag.text
        article += ' '.join(map(
            lambda tag: tag.text,
            soup.select_one('div.centralContent div.paragraph').select('p')
        ))
        article = unicodedata.normalize('NFKC', article).strip()
    except Exception:
        raise ValueError('Fail to parse CNA news article.')

    # News category.
    category = ''
    try:
        category = soup.select('div.breadcrumb > a')[1].text
        category = unicodedata.normalize('NFKC', category).strip()
    except Exception:
        # There may not have category.
        category = ''

    # News datetime.
    news_datetime = ''
    try:
        news_datetime = datetime.strptime(
            parsed_news.url.split('/')[-1][:8],
            '%Y%m%d',
        )
        # Convert to UTC.
        news_datetime = news_datetime - timedelta(hours=8)
        news_datetime = news_datetime.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        news_datetime = unicodedata.normalize('NFKC', news_datetime)
    except Exception:
        # There may not have category.
        news_datetime = ''

    # News reporter.
    reporter = ''
    try:
        match = REPORTER_PATTERN.match(article)
        reporter = article[match.start() + 1: match.end() - 1]
        article = article[match.end():]
    except Exception:
        # There may not have reporter.
        reporter = ''

    # News title.
    title = ''
    try:
        title = soup.select('div.centralContent h1 span')[0].text
        title = unicodedata.normalize('NFKC', title).strip()
    except Exception:
        raise ValueError('Fail to parse CNA news title.')

    parsed_news.article = article
    parsed_news.category = category
    parsed_news.company = '中央社'
    parsed_news.datetime = news_datetime
    parsed_news.reporter = reporter
    parsed_news.title = title
    return parsed_news
