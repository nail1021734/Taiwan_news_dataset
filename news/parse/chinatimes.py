import re
import unicodedata
from datetime import datetime, timedelta

from bs4 import BeautifulSoup

from news.crawlers.db.schema import RawNews
from news.parse.db.schema import ParsedNews


def parse(ori_news: RawNews) -> ParsedNews:
    """Parse Chinatimes news from raw HTML.

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
        article_tags = soup.select('div.article-body > p')

        if article_tags:
            # Remove empty tags.
            article = ' '.join(filter(
                bool,
                map(lambda tag: tag.text.strip(), article_tags)
            ))
        # One line only news. Chinatime is trash.
        else:
            article = soup.select('div.article-body')[0].text

        article = unicodedata.normalize('NFKC', article).strip()
    except Exception:
        raise ValueError('Fail to parse Chinatimes news article.')

    # News category.
    category = ''
    try:
        category = soup.select(
            'nav.breadcrumb-wrapper > ol > li > a > span'
        )[-1].text
        category = unicodedata.normalize('NFKC', category).strip()
    except Exception:
        # There may not have category.
        category = ''

    # News datetime.
    news_datetime = ''
    try:
        news_datetime = datetime.strptime(
            soup.select('header.article-header time[datetime]')[0]['datetime'],
            '%Y-%m-%d %H:%M',
        )
        # Convert to UTC.
        news_datetime = news_datetime - timedelta(hours=8)
        news_datetime = news_datetime.timestamp()
    except Exception:
        # There may not have category.
        news_datetime = ''

    # News reporter.
    reporter = ''
    try:
        reporter_tag = soup.select('div.author')[0]
        format_1 = reporter_tag.select('a')
        if format_1:
            reporter = format_1[0].text
        else:
            reporter = reporter_tag.text
        reporter = unicodedata.normalize('NFKC', reporter).strip()
    except Exception:
        # There may not have reporter.
        reporter = ''

    # News title.
    title = ''
    try:
        title = soup.select('h1.article-title')[0].text
        title = unicodedata.normalize('NFKC', title).strip()
    except Exception:
        raise ValueError('Fail to parse Chinatimes news title.')

    parsed_news.article = article
    parsed_news.category = category
    parsed_news.datetime = news_datetime
    parsed_news.reporter = reporter
    parsed_news.title = title
    return parsed_news
