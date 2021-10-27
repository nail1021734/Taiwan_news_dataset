import unicodedata
from datetime import datetime, timedelta

from bs4 import BeautifulSoup

from news.crawlers.db.schema import RawNews
from news.parse.db.schema import ParsedNews


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

    # News article.
    article = ''
    try:
        article_tags = soup.select(
            'div#article_inner_wrapper > article > div#CMS_wrapper > p[aid]'
        )
        for article_tag in article_tags:
            # Discard related news.
            for related_tag in article_tag.select('.related_copy_content'):
                related_tag.extract()
        # Joint remaining text.
        article = ' '.join(
            filter(
                bool,
                map(lambda tag: tag.text.strip(), article_tags),
            )
        )
        article = unicodedata.normalize('NFKC', article).strip()
    except Exception:
        raise ValueError('Fail to parse STORM news article.')

    # News category.
    category = ''
    try:
        category_tags = soup.select('div#title_tags_wrapper a')
        category = ','.join(map(lambda tag: tag.text.strip(), category_tags))
        category = unicodedata.normalize('NFKC', category).strip()
    except Exception:
        # There may not have category.
        category = ''

    # News datetime.
    timestamp = 0
    try:
        timestamp = datetime.strptime(
            soup.select('span#info_time')[0].text,
            '%Y-%m-%d %H:%M',
        )
        # Convert to UTC.
        timestamp = timestamp - timedelta(hours=8)
        timestamp = timestamp.timestamp()
    except Exception:
        # There may not have category.
        timestamp = 0

    # News reporter.
    reporter = ''
    try:
        reporter = soup.select('div#author_block span.info_author')[0].text
        reporter = unicodedata.normalize('NFKC', reporter).strip()
    except Exception:
        # There may not have reporter.
        reporter = ''

    # News title.
    title = ''
    try:
        title = soup.select('h1#article_title')[0].text
        title = unicodedata.normalize('NFKC', title).strip()
    except Exception:
        # storm response 404 with status code 200.
        # Thus some pages do not have title since it is 404.
        raise ValueError('Fail to parse STORM news title.')

    parsed_news.article = article
    parsed_news.category = category
    parsed_news.reporter = reporter
    parsed_news.timestamp = timestamp
    parsed_news.title = title
    return parsed_news
