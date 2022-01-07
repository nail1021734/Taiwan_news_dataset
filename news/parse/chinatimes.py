import re
import unicodedata
from datetime import datetime, timedelta
from typing import List

from bs4 import BeautifulSoup

from news.crawlers.db.schema import RawNews
from news.parse.db.schema import ParsedNews

BAD_ARTICLE_PATTERNS: List[re.Pattern] = [
    re.compile(r'文章來源:.*'),
    re.compile(r'----------------.*'),
    re.compile(r'更多內容.*'),
    re.compile(r'全文及圖表請見.*'),
    re.compile(r'圖片來源:.*'),
    re.compile(r'※免付費防疫專線.*'),
    re.compile(r' ★《中時新聞網》提醒您:'),
    re.compile(r' ★中時新聞網提醒您'),
]


def parser(raw_news: RawNews) -> ParsedNews:
    r"""Parse Chinatimes news from raw HTML."""
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
        article_tags = soup.select('div.article-body > p')

        if article_tags:
            # Remove empty tags.
            article = ' '.join(
                filter(bool, map(lambda tag: tag.text.strip(), article_tags))
            )
        # One line only news. Chinatime is trash.
        else:
            article = soup.select('div.article-body')[0].text

        article = unicodedata.normalize('NFKC', article).strip()
        for pattern in BAD_ARTICLE_PATTERNS:
            search_result = pattern.search(article)
            if search_result:
                article = article[:search_result.start()]
                break
    except Exception:
        raise ValueError('Fail to parse Chinatimes news article.')

    # News category.
    category = ''
    try:
        category = soup.select(
            'nav.breadcrumb-wrapper > ol > li > a > span',
        )[-1].text
        category = unicodedata.normalize('NFKC', category).strip()
    except Exception:
        # There may not have category.
        category = ''

    # News datetime.
    timestamp = ''
    try:
        timestamp = datetime.strptime(
            soup.select('header.article-header time[datetime]')[0]['datetime'],
            '%Y-%m-%d %H:%M',
        )
        # Convert to UTC.
        timestamp = timestamp - timedelta(hours=8)
        timestamp = timestamp.timestamp()
    except Exception:
        # There may not have category.
        timestamp = ''

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
    parsed_news.reporter = reporter
    parsed_news.timestamp = timestamp
    parsed_news.title = title
    return parsed_news
