import re
import unicodedata
from datetime import datetime, timedelta

from bs4 import BeautifulSoup

from news.db.schema import News

reporter_pattern = re.compile(r'\((.*?)/.*?報導\)')


def parse(ori_news: News) -> News:
    """Parse chinatimes news from raw HTML.

    Input news must contain `datetime`, `raw_xml` and `url` since these
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
    article = None
    try:
        article_tags = soup.select('div.article_body > p')
        # Remove empty tags.
        article = ' '.join(filter(
            bool,
            map(lambda tag: tag.text.strip(), article_tags)
        ))
        article = unicodedata.normalize('NFKC', article)
    except Exception:
        raise ValueError('Fail to parse chinatimes news article.')

    # News category.
    category = None
    try:
        category = soup.select(
            'nav.breadcrumb-wrapper > ol > li > a > span'
        )[-1].text
        category = unicodedata.normalize('NFKC', category)
    except Exception:
        # There may not have category.
        pass

    # News datetime.
    news_datetime = None
    try:
        news_datetime = datetime.strptime(
            soup.select('header.article-header time[datetime]')['datetime'],
            '%Y-%m-%d %H:%M',
        )
        # Convert to UTC.
        news_datetime = news_datetime - timedelta(hours=8)
        news_datetime = news_datetime.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        news_datetime = unicodedata.normalize('NFKC', news_datetime)
    except Exception:
        # There may not have category.
        news_datetime = None

    # News reporter.
    reporter = None
    try:
        reporter = soup.select('div.author > a')[0].text
        reporter = unicodedata.normalize('NFKC', reporter)
    except Exception:
        # There may not have reporter.
        reporter = None

    # News title.
    title = None
    try:
        title = soup.select('h1.article-title')[0].text
        title = unicodedata.normalize('NFKC', title)
    except Exception:
        raise ValueError('Fail to parse chinatimes news title.')

    parsed_news.article = article
    parsed_news.category = category
    parsed_news.company = '中時'
    parsed_news.datetime = news_datetime
    parsed_news.reporter = reporter
    parsed_news.title = title
    return parsed_news
