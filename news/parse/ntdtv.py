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
]
REPORTER_PATTERNS = [
    re.compile(r'\(記者(.*?)(?:綜合|整理)?報導/.*?\)'),
    re.compile(r'\(記者(.*?)/.*?\)'),
    re.compile(r'新唐人記者\s*(.*?)(?:綜合|整理)?報導'),
    re.compile(r'新唐人(.*?)(?:綜合|整理)?報導'),
    re.compile(r'^採訪/(.*?)\s*編輯/(.*?)\s*後製/(.*?)$'),
    re.compile(r'\(責任編輯:(.*?)\)')
]
URL_PATTERN = re.compile(r'/b5/(\d+)/(\d+)/(\d+)/a\d+.html')


def parser(raw_news: Final[RawNews]) -> ParsedNews:
    """Parse ntdtv news from raw HTML.

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
        soup = BeautifulSoup(raw_news.raw_xml, 'html.parser')
    except Exception:
        raise ValueError('Invalid html format.')

    # News article.
    article = ''
    try:
        article_tags = []
        # Drop p tags if they are related news.
        for tag in soup.select('div[itemprop=articleBody].post_content > p'):
            if '【熱門話題】' in tag.text:
                break
            elif '相關鏈接：' in tag.text:
                break
            article_tags.append(tag)
        article = ' '.join(map(lambda tag: tag.text.strip(), article_tags))
        article = unicodedata.normalize('NFKC', article).strip()
        for pattern in BAD_ARTICLE_PATTERNS:
            article = pattern.sub('', article).strip()
    except Exception:
        raise ValueError('Fail to parse ntdtv news article.')

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
            f"{year:04d}-{month:02d}-{day:02d}T00:00:00Z"
        )
        news_datetime = news_datetime.timestamp()
    except Exception:
        # There may not have category.
        news_datetime = ''

    # News reporter.
    reporter = ''
    try:
        paragraphs = article.split(' ')
        for pattern in REPORTER_PATTERNS:
            match = pattern.match(paragraphs[-1])
            if match:
                reporter = ','.join(match.groups())
                article = ' '.join(paragraphs[:-1])
                break

            match = pattern.match(' '.join(paragraphs[-2:]))
            if match:
                reporter = ','.join(match.groups())
                article = ' '.join(paragraphs[:-2])
                break
    except Exception:
        # There may not have reporter.
        reporter = ''

    # News title.
    title = ''
    try:
        title = soup.select('div.article_title > h1')[0].text
        title = unicodedata.normalize('NFKC', title).strip()
        # Discard trash news.
        if '【熱門話題】' in title:
            article = ''
        for pattern in BAD_TITLE_PATTERNS:
            title = pattern.sub('', title)
    except Exception:
        raise ValueError('Fail to parse ntdtv news title.')

    parsed_news.article = article
    parsed_news.category = category
    parsed_news.datetime = news_datetime
    parsed_news.reporter = reporter
    parsed_news.title = title
    return parsed_news
