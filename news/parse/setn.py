import re
import unicodedata
from datetime import datetime, timedelta

from bs4 import BeautifulSoup

from news.crawlers.db.schema import RawNews
from news.parse.db.schema import ParsedNews

CATEGORIES = {
    0: '熱門',
    2: '財經',
    4: '生活',
    5: '國際',
    6: '政治',
    7: '科技',
    8: '娛樂',
    9: '名家專欄',
    12: '汽車',
    17: '華流',
    34: '運動',
    41: '社會',
    42: '新奇',
    45: '日韓',
    46: '音樂',
    47: '寵物',
    50: '旅遊',
    52: '女孩',
    54: '房產',
    65: '健康',
}

END_ARTICLE_PATTERNS = [
    re.compile(r'※ 免付費防疫專線.*'),
]

REPORTER_PATTERNS = [
    re.compile(r'^記者(.*?)/.*?報導'),
    re.compile(r'^.*?/(.*?)報導'),
    re.compile(r'^影音編輯/(.*?) '),
    re.compile(r'^助理編輯/(.*?) '),
]


def parse(ori_news: RawNews) -> ParsedNews:
    """Parse SET news from raw HTML.

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
        article_tags = soup.select('div#Content1 > p:not([class]):not([style])')
        # Joint remaining text.
        article = ' '.join(
            filter(
                bool,
                map(lambda tag: tag.text.strip(), article_tags),
            )
        )
        article = unicodedata.normalize('NFKC', article).strip()
        for pattern in END_ARTICLE_PATTERNS:
            search_result = pattern.search(article)
            if search_result:
                article = article[:search_result.start()]
                break
        article = article.strip()
    except Exception:
        raise ValueError('Fail to parse SET news article.')

    # News category.
    category = ''
    try:
        category = CATEGORIES[soup.select(
            'input[type=hidden]#pageGroupID, input[type=hidden]#hfPageGroupId'
        )[0]['value']]
        category = unicodedata.normalize('NFKC', category).strip()
    except Exception:
        # There may not have category.
        category = ''

    # News datetime.
    news_datetime = ''
    try:
        time_tag = soup.select('time.page-date')[0]
        news_datetime = datetime.strptime(time_tag.text, '%Y/%m/%d %H:%M:%S')
        # Convert to UTC.
        news_datetime = news_datetime - timedelta(hours=8)
        news_datetime = news_datetime.timestamp()
    except Exception:
        # There may not have category.
        news_datetime = ''

    # News reporter.
    reporter = ''
    try:
        for pattern in REPORTER_PATTERNS:
            match = pattern.match(article)
            if match:
                reporter = ','.join(match.groups())
                article = article[:match.start()] + article[match.end():]
                article = article.strip()
                break
    except Exception:
        # There may not have reporter.
        reporter = ''

    # News title.
    title = ''
    try:
        title = soup.select('h1.news-title-3')[0].text
        title = unicodedata.normalize('NFKC', title).strip()
    except Exception:
        raise ValueError('Fail to parse SET news title.')

    parsed_news.article = article
    parsed_news.category = category
    parsed_news.datetime = news_datetime
    parsed_news.reporter = reporter
    parsed_news.title = title
    return parsed_news
