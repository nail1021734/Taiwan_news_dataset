import re
import unicodedata
from datetime import datetime, timedelta
from typing import Final

from bs4 import BeautifulSoup

from news.crawlers.db.schema import RawNews
from news.parse.db.schema import ParsedNews

REMOVE_XML_PATTERN = re.compile(
    r'<blockquote\s.*?>.*?<a\s.*?>\.\.\.more</a>.*?</blockquote>'
)

REMOVE_ARTICLE_PATTERNS = [
    re.compile(r'（延伸閱讀：.*?）'),
    re.compile(r'...more'),
]


def parser(raw_news: Final[RawNews]) -> ParsedNews:
    """Parse UDN news from raw HTML.

    Input news must contain `raw_xml` and `url` since these
    information cannot be retrieved from `raw_xml`.
    """
    # Information which cannot be parsed.
    parsed_news = ParsedNews(
        url_pattern=raw_news.url_pattern,
        company_id=raw_news.company_id,
    )

    soup = None
    try:
        # UDN formatting sucks.
        # raw_xml = REMOVE_XML_PATTERN.sub('', raw_news.raw_xml)
        raw_xml = raw_news.raw_xml
        raw_xml = re.sub(
            r'<blockquote',
            r'</p><blockquote',
            raw_xml,
        )
        raw_xml = re.sub(
            r'</blockquote>',
            r'</blockquote><p>',
            raw_xml,
        )
        soup = BeautifulSoup(raw_xml, 'html.parser')
        # soup = BeautifulSoup(raw_news.raw_xml, 'html.parser')
    except Exception:
        raise ValueError('Invalid html format.')

    # News article.
    article = ''
    try:
        # Discard images, captions, styles, scripts and ads.
        for tag in soup.select(
                'figure.article-content__image, style, script, div.inline-ads'):
            tag.extract()

        # Discard related links.
        for blockquote_tag in soup.select('blockquote'):
            for a_tag in blockquote_tag.select('a'):
                if a_tag.text.strip() == '...more':
                    blockquote_tag.extract()
                    break

        article_tags = soup.select(
            'section.article-content__editor > p, section.article-content__editor > blockquote'
        )
        article = ' '.join(map(lambda tag: tag.text.strip(), article_tags))

        for pattern in REMOVE_ARTICLE_PATTERNS:
            article = pattern.sub('', article)
        article = unicodedata.normalize('NFKC', article).strip()
    except Exception:
        raise ValueError('Fail to parse UDN news article.')

    # News category.
    category = ''
    try:
        category = soup.select(
            'nav.article-content__breadcrumb > a.breadcrumb-items'
        )[-2].text
        category = unicodedata.normalize('NFKC', category).strip()
    except Exception:
        # There may not have category.
        category = ''

    # News datetime.
    news_datetime = ''
    try:
        news_datetime = soup.select(
            'section.authors > time.article-content__time'
        )[0].text
        # Convert to UTC.
        news_datetime = datetime.strptime(
            news_datetime,
            '%Y-%m-%d %H:%M',
        ) - timedelta(hours=8)
        news_datetime = news_datetime.timestamp()
    except Exception:
        # There may not have category.
        news_datetime = ''

    # News reporter.
    reporter = ''
    try:
        reporter_tags = soup.select(
            'section.authors > span.article-content__author > a'
        )
        reporter = ','.join(map(lambda tag: tag.text, reporter_tags))
        reporter = unicodedata.normalize('NFKC', reporter).strip()
    except Exception:
        # There may not have reporter.
        reporter = ''

    # News title.
    title = ''
    try:
        title = soup.select('h1.article-content__title')[0].text
        title = unicodedata.normalize('NFKC', title).strip()
    except Exception:
        # Some pages do not have title since we are not VIP.
        raise ValueError('Fail to parse UDN news title.')

    parsed_news.article = article
    parsed_news.category = category
    parsed_news.datetime = news_datetime
    parsed_news.reporter = reporter
    parsed_news.title = title
    return parsed_news
