import re
import unicodedata
from datetime import datetime

from bs4 import BeautifulSoup

from news.crawlers.db.schema import RawNews
from news.parse.db.schema import ParsedNews

REPORTER_END_PATTERNS = [
    re
    .compile(r'[。!\s]\s*\(.{0,6}/([^(綜合|整理)]{0,16})\s+.{0,4}(:?報導|編輯)\){0,2}'),
    re.compile(r'[。!\s]\s*.{0,6}/([^(綜合|整理)]{0,16})\s*.{0,4}(:?報導|編輯)'),
    re.compile(r'\(責任編輯/(.*?)\)'),
    # (民視新聞/鄭博暉、林俊明、洪明生 台南-屏東)
    re.compile(r'[。!\s]\s*\(.{0,6}/([^(綜合|整理)]{0,16})\s+.{0,10}\){0,2}'),
]

REPORTER_BEGIN_PATTERNS = [
    re.compile(r'^【.{0,6}\s+([^(綜合|整理)]*?)/.{0,4}(:?報導|編輯)】'),
    re.compile(r'^【.{0,6}/記者([^(綜合|整理)]*?)(:?報導|編輯)】'),
    re.compile(r'^.{0,6}/([^(綜合|整理)]{0,10})(:?報導|編輯)'),
]

BAD_TITLE_PATTERNS = [
    re.compile(r'MLB/'),
    re.compile(r'P\.LEAGUE\+/'),
    re.compile(r'法網/'),
    re.compile(r'快新聞/'),
    re.compile(r'→'),
    re.compile(r'LIVE/'),
    re.compile(r'NBA/'),
    re.compile(r'影/'),
    re.compile(r'有影/'),
]

BAD_ARTICLE_PATTERNS = [
    re.compile(r'^.{0,6}/(.{0,10})(:?報導|編輯)'),
    re.compile(r'文章轉載自:.*'),
    re.compile(r'文章授權:.*'),
    re.compile(r'延伸閱讀:.*'),
    re.compile(r'【延伸閱讀】.*'),
    re.compile(r'更多古典樂新訊息:.*'),
    re.compile(r'\(中央社\)'),
    re.compile(r'影片轉載自:.*'),
    re.compile(r'\(民視新聞(網)?[\s/]綜合報導\)'),
    re.compile(r'\(\w*?報導\)'),
    re.compile(r'※ 免付費防疫專線:.*'),
    re.compile(r'更多最新消息.*'),
    re.compile(r'就❤NOW健康:.*'),
    re.compile(r'《(:?民視快新聞|民視新聞網)》提醒您:.*'),
    re.compile(r'更多NOW健康報導.*'),
    re.compile(r'★.*'),
    re.compile(r' ◆ .*'),
    re.compile(r'更多精彩的詳細影片:.*'),
    re.compile(r'全部照片,請見臉書社團.*'),
    re.compile(r'所有精彩節目內容.*'),
    re.compile(r'❤?【NOW健康】關心您:.*'),
    re.compile(r'現場最新情形請鎖定《民視快新聞》直播.*'),
    re.compile(r'-{5,}.*?-{5,}'),
    re.compile(r'【看更多】.*'),
    re.compile(r'・'),
    re.compile(r'民視新聞網關心您.*'),
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


def parser(raw_news: RawNews) -> ParsedNews:
    """Parse FTV news from raw HTML.

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
        article_tags = soup.select('div#preface > p, div#newscontent > p')
        article = ' '.join(p_tag.text.strip() for p_tag in article_tags)
        article = unicodedata.normalize('NFKC', article).strip()
    except Exception:
        raise ValueError('Fail to parse FTV news article.')
    # News category.
    category = ''
    try:
        category_word = parsed_news.url_pattern.split('/')[-1][7]
        category = CATEGORIES[category_word]
    except Exception:
        # There may not have category.
        category = ''

    # News datetime.
    timestamp = 0
    try:
        url_datetime = parsed_news.url_pattern.split('/')[-1][:7]
        url_datetime = f'{url_datetime[:4]}' + \
            f'{int("0x" + url_datetime[4], 0):02}{url_datetime[5:]}'
        timestamp = datetime.strptime(
            url_datetime,
            '%Y%m%d',
        )
        timestamp = timestamp.timestamp()
    except Exception:
        # There may not have category.
        timestamp = 0

    # News reporter.
    reporter = ''
    try:
        for pattern in REPORTER_BEGIN_PATTERNS:
            match = pattern.match(article)
            if match:
                reporter = match.group(1).strip()
                article = article[match.end():].strip()
                break
        if not reporter:
            for pattern in REPORTER_END_PATTERNS:
                match = pattern.search(article)
                if match:
                    reporter = match.group(1).strip()
                    article = article[:match.start()].strip()
                    break

    except Exception:
        # There may not have reporter.
        reporter = ''

    # Filter article bad pattern.
    try:
        for pattern in BAD_ARTICLE_PATTERNS:
            article = pattern.sub('', article)
        article = re.sub(r'\s+', ' ', article).strip()

        # If article is not end with period.
        if article and not re.match('[。!?]', article[-1]):
            article = article + '。'
    except Exception:
        raise ValueError('Fail to parse FTV news article.')

    # News title.
    title = ''
    try:
        title = soup.select('div.col-article > h1.text-center')[0].text
        title = unicodedata.normalize('NFKC', title).strip()
        for pattern in BAD_TITLE_PATTERNS:
            match = pattern.search(title)
            if match:
                title = title[:match.start()] + title[match.end():]
    except Exception:
        # FTV response 404 with status code 200.
        # Thus some pages do not have title since it is 404.
        raise ValueError('Fail to parse FTV news title.')

    parsed_news.article = article
    parsed_news.category = category
    parsed_news.reporter = reporter
    parsed_news.timestamp = timestamp
    parsed_news.title = title
    return parsed_news
