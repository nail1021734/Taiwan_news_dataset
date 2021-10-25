import re
import unicodedata
from datetime import timedelta
from typing import Final

import bs4
import dateutil.parser
from bs4 import BeautifulSoup

from news.crawlers.db.schema import RawNews
from news.parse.db.schema import ParsedNews

DROP_ARTICLE_PATTERNS = [
    re.compile(r'因應新冠肺炎疫情，疾管署持續疫情監測與邊境管制措施，'),
    re.compile(r'◎\s*本文摘自'),
    re.compile(r'◎\s*圖片來源'),
    re.compile(r'〈首圖出處'),
    re.compile(r'《TVBS》提醒您'),
]

REMOVE_ARTICLE_PATTERNS = [
    re.compile(r'（中央社）'),
    re.compile(r'最HOT話題在這！想跟上時事，快點我加入TVBS新聞LINE好友！'),
    re.compile(
        r'《TVBS》提醒您：因應新冠肺炎疫情，疾管署持續疫情監測與邊境管制措施，如有疑似症狀，請撥打：1922專線，或 0800-001922。'
    ),
    re.compile(r'(?:實習)?編輯／.*?$'),
]

CATEGORIES = {
    'local': '社會',
    'life': '生活',
    'world': '國際',
    'entertainment': '娛樂',
    'china': '中國',
    'politics': '政治',
    'sports': '運動',
    'tech': '科技',
    'focus': '焦點',
    'fun': '新奇',
    'travel': '旅遊',
    'health': '健康',
    'cars': '車',
    'money': '財經',
}
CATEGORY_PATTERN = re.compile(r'/(.*?)/\d+')


def parser(raw_news: Final[RawNews]) -> ParsedNews:
    """Parse TVBS news from raw HTML.

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
        article_node = soup.select('div#news_detail_div > html > body')[0]
        # Discard image, caption and related news.
        for tag in article_node.select('div.img, div[style], span.endtext, b'):
            tag.extract()

        # # Strong tags and styled text.
        # for tag in article_node.select('span[style], strong'):

        # Get remaining text.
        for node in article_node.children:
            if isinstance(node, bs4.element.Tag):
                text = node.text
            else:
                text = str(node)

            # Drop following text if pattern matched.
            for pattern in DROP_ARTICLE_PATTERNS:
                drop_pattern_match = pattern.match(text)
                if drop_pattern_match:
                    text = ''
                    break

            if drop_pattern_match:
                break

            # Remove text if pattern matched.
            for pattern in REMOVE_ARTICLE_PATTERNS:
                text = pattern.sub('', text)

            if text:
                article += text + ' '

        article = unicodedata.normalize('NFKC', article).strip()
    except Exception:
        raise ValueError('Fail to parse TVBS news article.')

    # News category.
    category = ''
    try:
        category = CATEGORIES[CATEGORY_PATTERN.match(parsed_news.url_pattern
                                                    ).group(1)]
        category = unicodedata.normalize('NFKC', category).strip()
    except Exception:
        # There may not have category.
        category = ''

    # News datetime.
    news_datetime = ''
    try:
        # Convert to UTC.
        news_datetime = dateutil.parser.isoparse(
            soup.select('meta[name=pubdate]')[0]['content']
        ) - timedelta(hours=8)
        news_datetime = news_datetime.timestamp()
    except Exception:
        # There may not have category.
        news_datetime = ''

    # News reporter.
    reporter = ''
    try:
        reporter = soup.select('div.author_box > div.author > a')[0].text
        reporter = unicodedata.normalize('NFKC', reporter).strip()
    except Exception:
        # There may not have reporter.
        reporter = ''

    # News title.
    title = ''
    try:
        title = soup.select('div.title_box > h1.title')[0].text
        title = unicodedata.normalize('NFKC', title).strip()
    except Exception:
        # storm response 404 with status code 200.
        # Thus some pages do not have title since it is 404.
        raise ValueError('Fail to parse TVBS news title.')

    parsed_news.article = article
    parsed_news.category = category
    parsed_news.datetime = news_datetime
    parsed_news.reporter = reporter
    parsed_news.title = title
    return parsed_news
