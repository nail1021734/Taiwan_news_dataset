import re
import unicodedata
from datetime import datetime, timedelta

from bs4 import BeautifulSoup

from news.db.schema import News

REPORTER_END_PATTERNS = [
    re.compile(r'\(.{0,6}/(.{0,12})\s+.{0,4}(:?報導|編輯)\){0,2}'),
    re.compile(r'.{0,6}/(.{0,12})\s*.{0,4}(:?報導|編輯)'),
    re.compile(r'\(.{0,6}/(.{0,12})\s+.{0,4}.{0,6}\){0,2}'),# (民視新聞/鄭博暉、林俊明、洪明生 台南-屏東)
]

REPORTER_BEGIN_PATTERNS = [
    re.compile(r'^.{0,6}/(.*?)(:?報導|編輯)'),
]

BAD_ARTICLE_PATTERNS = [
    re.compile(r'文章轉載自:.*'),
    re.compile(r'文章授權:.*'),
    re.compile(r'延伸閱讀:.*'),
    re.compile(r'更多古典樂新訊息:.*'),
    re.compile(r'\(中央社\)'),
    re.compile(r'影片轉載自:.*'),
    re.compile(r'\(民視新聞網 綜合報導\)'),
    re.compile(r'\(\w*報導\)')
]

CATEGORIES = {
    'A': '體育',
    'C': '一般',
    'F': '財經',
    'I': '國際',
    'J': '美食',
    'L': '生活',
    'N': '社會',
    'P': '政治',
    'R': '美食',
    'S': '社會',
    'U': '社會',
    'W': '一般',
}


def parse(ori_news: News) -> News:
    """Parse FTV news from raw HTML.

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
        article_tags = soup.select(
            'article#contentarea[itemprop=articleBody] div#preface p'
        )
        article_tags.extend(soup.select(
            'article#contentarea[itemprop=articleBody] div#newscontent p'
        ))
        article = ' '.join(p_tag.text.strip() for p_tag in article_tags)
        article = unicodedata.normalize('NFKC', article).strip()
        for pattern in BAD_ARTICLE_PATTERNS:
            article = pattern.sub('', article).strip()
    except Exception:
        raise ValueError('Fail to parse FTV news article.')

    # News category.
    category = ''
    try:
        category_word = parsed_news.url.split('/')[-1][7]
        category = CATEGORIES[category_word]
    except Exception:
        # There may not have category.
        category = ''

    # News datetime.
    news_datetime = ''
    try:
        news_datetime = datetime.strptime(
            soup.select('li.date')[0].text.strip(),
            '%Y/%m/%d %H:%M:%S',
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
        for pattern in REPORTER_BEGIN_PATTERNS:
            match = pattern.match(article)
            if match:
                reporter = match.group(1)
                article = article[match.end():].strip()
                break
        for pattern in REPORTER_END_PATTERNS:
            match = pattern.search(article)
            if match:
                reporter = match.group(1)
                article = article[:match.start()].strip()
                break

    except Exception:
        # There may not have reporter.
        reporter = ''

    # News title.
    title = ''
    try:
        title = soup.select('div.col-article > h1.text-center')[0].text
        title = unicodedata.normalize('NFKC', title).strip()
    except Exception:
        # storm response 404 with status code 200.
        # Thus some pages do not have title since it is 404.
        raise ValueError('Fail to parse FTV news title.')

    parsed_news.article = article
    parsed_news.category = category
    parsed_news.company = '民視'
    parsed_news.datetime = news_datetime
    parsed_news.reporter = reporter
    parsed_news.title = title
    return parsed_news
