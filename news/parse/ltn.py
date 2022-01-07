import re
import unicodedata
from datetime import datetime, timedelta

import bs4
from bs4 import BeautifulSoup

from news.crawlers.db.schema import RawNews
from news.parse.db.schema import ParsedNews

BAD_ARTICLE_PATTERNS = [
    re.compile(r'^首次上稿.*?\d+:\d+$'),
    re.compile(r'^更新時間.*?\d+:\d+$'),
]

REPORTER_PATTERNS = [
    re.compile(r'〔記者(.*?)/.*?〕'),
    re.compile(r'〔記者(.*?)〕'),
    re.compile(r'〔編譯(.*?)/.*?〕'),
    re.compile(r'〔編譯(.*?)〕'),
    re.compile(r'〔(.*?)/.*?報導〕'),
    re.compile(r'\[記者(.*?)/.*?\]'),
    re.compile(r'\[記者(.*?)\]'),
    re.compile(r'\[編譯(.*?)/.*?\]'),
    re.compile(r'\[編譯(.*?)\]'),
    re.compile(r'\[(.*?)/.*?報導\]'),
    re.compile(r'記者(.*?)/.*?'),
    re.compile(r'編譯(.*?)/.*?'),
    re.compile(r'〔(.*?)/.*?〕'),
    re.compile(r'〔(.*?)〕'),
    re.compile(r'(.*?)/.*?'),
    re.compile(r'◎(.*?)\s+'),
]


def parser(raw_news: RawNews) -> ParsedNews:
    """Parse ltn news from raw HTML.

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
            'div[itemprop=articleBody] div.boxText.text.boxTitle '
            + '> p:not([class])'
        )
        # Drop all p tags after related news.
        related_news_tag = list(
            filter(
                lambda tag: isinstance(tag.previous_sibling, bs4.element.Tag)
                and '相關新聞' in tag.previous_sibling.text,
                article_tags,
            )
        )
        if related_news_tag:
            article_tags = article_tags[:article_tags.idx(related_news_tag[0])]
        article_tags = filter(
            lambda tag: all(
                map(
                    lambda pattern: not bool(pattern.match(tag.text.strip())),
                    BAD_ARTICLE_PATTERNS,
                )
            ), article_tags
        )

        article = ' '.join([i.text.strip() for i in article_tags])
        article = unicodedata.normalize('NFKC', article).strip()
    except Exception:
        raise ValueError('Fail to parse ltn news article.')

    # News category.
    category = ''
    try:
        category = soup.select('div.breadcrumbs > a')[-1].text
        category = unicodedata.normalize('NFKC', category).strip()
    except Exception:
        # There may not have category.
        category = ''

    # News datetime.
    timestamp = 0
    try:
        timestamp = datetime.strptime(
            soup.select('div.text.boxTitle.boxText > span.time')[0].text,
            ' %Y/%m/%d %H:%M',
        )
        # Convert to UTC.
        timestamp = timestamp - timedelta(hours=8)
        timestamp = timestamp.timestamp()
    except Exception:
        # There may not have category.
        timestamp = 0

    reporter = ''
    try:
        for pattern in REPORTER_PATTERNS:
            match = pattern.search(article)
            if match:
                reporter = match.group(1)
                article = article[:match.start()] + article[match.end():]
                break
    except Exception:
        # There may not have reporter.
        reporter = ''

    # News title.
    title = ''
    try:
        title = soup.select('div.whitecon > h1')[0].text
        title = unicodedata.normalize('NFKC', title).strip()
    except Exception:
        raise ValueError('Fail to parse ltn news title.')

    parsed_news.article = article
    parsed_news.category = category
    parsed_news.reporter = reporter
    parsed_news.timestamp = timestamp
    parsed_news.title = title
    return parsed_news
