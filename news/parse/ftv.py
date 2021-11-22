import re
from datetime import datetime
from functools import partial

from bs4 import BeautifulSoup

from news.crawlers.db.schema import RawNews
from news.parse.db.schema import ParsedNews
from news.parse.util.normalize import NFKC

TEXT_FILTER = [
    # remove acsii and unicdoe control characters
    partial(
        re.compile(r'[\x00-\x1f\x7f-\x9f\u0300-\u036F\uE000-\uF8FF]').sub,
        repl=''
    ),
    # normalize similar characters
    partial(re.compile(r'[─—]').sub, repl='-'),
    partial(re.compile(r'[〈〔]').sub, repl='('),
    partial(re.compile(r'[〉〕]').sub, repl=')'),
    partial(re.compile(r'╱').sub, repl='/'),
    # merge repeated spaces
    partial(re.compile(r'\s+').sub, repl=' '),
]

# yapf: disable
LOCATIONS = [
    # only list cities in taiwan,
    # it's not realistic to list all cities in the world
    # a post filter by dictionary lookup might be required for further cleanup
    '基隆', '新北', '北市', '台北', '雙北',
    '桃園', '新竹', '苗栗',
    '台中', '彰化', '南投', '中部',
    '雲林', '嘉義', '屏東',
    '台南', '高雄', '南部', '南市',
    '宜蘭', '花蓮', '台東',
    '澎湖', '金門', '馬祖',
    # frequent contries
    '美國', '日本', '韓國', '英國', '德國', '印尼', '越南', '印度', '中國', '帛琉',
    # other stuff may appear
    '綜合', '採訪', '專題', 'SNG', '小組',
]
# yapf: enable

REPORTER_PATTERNS = [
    # remove common pattern which has no reporter
    # 100403
    re.compile(r'(?:^|\()\s*(?:民視新聞網?|國際中心)\s*/?\s*(?:(?:綜合|專題)?報導|編譯|工商好消息|新聞來源:中央社)\s*\)?()'),

    # common pattern for bracket inclosed pattern ended with location
    # (民視新聞網?/AAA BBB CCC LOCATIONS)
    re.compile(
        # left bracket
        r'\s?\(\s?' +

        # ftv name
        r'(?:民\s?視(?:/?新聞?網?報?|記者|異言堂)+|快新聞)\s?'+

        # it might have separator and one leading typo or none
        r'(?:.?/)?\s?' +

        # reporter, non greedy modifier is required for clean result
        # the reporter could be empty which have location only
        r'([^\)/]{0,20}?)\s?' +

        # generated pattern for locations
        r'[/、]*(?:(?:{locations})[縣市、\s-]*)+'.format(locations='|'.join(LOCATIONS)) +

        # ended pattern
        r'\S{0,4}?(?:報導)?\S{,2}'  +

        # right bracket or end of text
        r'\s?(?:[\)\s]+|$)'

    ), # total 97455
    # without reporter 1359

    # start with XX中心
    re.compile(
        r'^\(?\S{0,2}中心?\s*/' +
        r'\s*(\S{,10}?)\s*' +
        r'(?:(?:{locations})[縣市、\s-]*)*'.format(locations='|'.join(LOCATIONS)) +
        r'報導\)?'
    ), # 14644

    # common pattern for bracket inclosed pattern ended without location
    # 2181
    re.compile(r'\(\s*民視新聞網?\s*/\s*(.{0,16}?)\s?(?:專題|綜合|綜|合|民視新聞網)?(?:專訪|報導)*\s*\)\s*'),
    # 1806
    re.compile(r'^【NOW健康 (\S{,10}?)(?:編譯組|編輯部)?/\S{1,4}報導】'),
    # 1636
    re.compile(r'^【+\s*健康醫療網\s*/\s*(?:編輯部整理)?(?:記者)?(\S{,10}?)(?:外電|綜合|報導)*\s*】+'),
    re.compile(
        r'^記者(\S{,7})' + \
        r'\s*/\s*(?:(?:{locations})[縣市]?)?(?:獨家)?報導'.format(locations='|'.join(LOCATIONS))
        ), # 464

    # 3685
    re.compile(r'\(?\s*四季線上\s*/+\s*(.{0,16}?)\s*(?:綜合|整理)*(?:編輯|報導)\s*\)?(?:\s*|$)'),
    # 97
    re.compile(r'\(?責任編輯/(.{,7}?)(?:\)|\s|$)'),
    # 16
    re.compile(
        r'[。!\s]\s*\(.{0,6}/([^(綜合|整理)]{0,16})\s+.{0,4}(:?報導|編輯)\){0,2}'),
    # 192
    re.compile(r'[。!\s]\s*.{0,6}/([^(綜合|整理)]{0,16})\s*.{0,4}(:?報導|編輯).{,2}$'),
    # 21
    re.compile(r'[。!\s]\s*\(.{0,6}/([^(綜合|整理)]{0,16})\s+.{0,10}\).{,2}$'),
    # 23053 not matched to any pattern
]

BAD_TITLE_PATTERNS = [
    # number of matches from 245653 news
    # types & projects
    re.compile(r'^(快新聞|快訊|夜線|LIVE)/', re.IGNORECASE),  # 38831
    re.compile(r'^(異言堂|事實查核|新聞觀測站)/'),  # 700
    # categories
    re.compile(r'^(全球|MLB|NBA|中職|日職|3C)/'),  # 3629
    # events
    re.compile(r'^(東奧|武漢肺炎)/'),  # 1752
    re.compile(r'^\[\d{4}/\d{2}/\d{2}\]'),  # 838
    re.compile(r'^P\.LEAGUE\+?/'),  # 178
    # other
    re.compile(r'^(影|獨)/'),  # 454
    re.compile(r'^[不斷最]*更?新/'),  # 73
    re.compile(r'^[^/0-9]{1,6}/'),  # 2423 match other infrequent subpattern
]

CARELINES = [
    r'安心專線:1925\(依舊愛我\)',
    '張老師專線:1980',
    '提醒您:不良行為,請勿模仿!',
    r'生命線(?:協談)?專線:1995',
    '教育部反霸凌投訴專線:0800-200-885',
    r'「iWIN網路防護機構」網安專線\s?:\s?\(02\)2577-5118[\s,]*服務時間:週一至週五 9:00~18:00',
    '防範武漢肺炎,肥皂勤洗手、必要時戴口罩、避免食用生肉及生蛋、少去人多的場所、避免接觸禽畜類動物!回國若身體不適請主動通報,14天內出現疑似症狀請先撥打防疫專線,並戴上口罩儘速就醫,務必告知醫師旅遊史。',
]

BAD_ARTICLE_PATTERNS = [
    re.compile(
        r'\(?\s*(?:資料來源:|網址:)?\s*https?://[A-Za-z0-9-._~:/?#\[\]@!$&\'()*+,;%=]+\s*\)?'
    ),
    re.compile(r'\(新聞來源.{,10}民視新聞網報導\)'),
    re.compile(r'文章(?:轉載自|授權|來源):.*'),
    re.compile(
        r'\s?(?:《?(?:民視快新聞|民視新聞網?)》?(?:提醒|關心)您[:\s]*)?'
        + r'(?:[◆\s]*(?:{txts}))+'.format(txts='|'.join(CARELINES)),
    ),
    re.compile(r'《(:?民視快新聞|民視新聞網)》提醒您:.{,120}[。!$]'),
    re.compile(r'\(本文由.{1,20}?授權.{1,20}?\)'),
    re.compile(r'\(?本文由(.{,10}?)授權.{1,15}$'),
    re.compile(r'【(?:Youtube觀看|Facebook觀看)】'),
    re.compile(r'(?:所有|更多|詳細)+(?:精彩|的)*(?:詳細|節目|內容|影片|節目|報導)+.{,80}$'),
    re.compile(r'更多古典樂新訊息:.*'),
    re.compile(r'【掌握武漢肺炎數據[^】]+?】'),
    re.compile(r'\((?:中央社|民視新聞網|中央社|綜合|四季線上)(?:報導)?\)'),
    re.compile(r'\(民視(?:網路)?新聞網?[\s/]?(?:綜合|中心)報導\)'),
    re.compile(r'\(\S*?報導\)$'),
    re.compile(r'(?:民視新聞網關心您|※ 免付費防疫專線:).{,80}$'),
    re.compile(r'更多疫情最新消息,請持續鎖定《民視快新聞》。'),
    re.compile(r'(?:點擊藍標可觀看完整報導;)?更多最新消息請鎖定民視【2300夜線新聞】!?'),
    re.compile(r'(?:資料來源:健康醫療網\s*|更多健康資訊:健康醫療網\s*|喜歡本文請按讚並分享給好友!\s*)+'),
    re.compile(
        r'《民視新聞關心您》自殺不能解決問題,勇敢求救並非弱者,社會處處有溫暖,一定能度過難關。自殺防治諮詢安心專線:0800-788995'
    ),
    re.compile(r'\(圖/[^\)]{1,20}提供\)'),
    re.compile(r'\(授權自\S{1,20}\)$'),
    re.compile(r'\(文章授權提供/.{,15}\)'),
    re.compile(r'更多最新消息請鎖定民視新聞台【\S{1,16}】!'),
    re.compile(r'(?:(?:就❤|更多|❤)【?NOW健康】?(?:報導|關心您)?[:▸].{,80})+$'),
    re.compile(r'現場最新情形請鎖定《民視快新聞》直播(?:,帶您掌握最新訊息)?。'),
    re.compile(r'-{3,}.{,20}?-{3,}'),
    re.compile(r'【看更多】.{,80}$'),
    re.compile(r'(?:【?推薦閱讀】?.{,80}?)+$'),
    re.compile(r'[\(]延伸閱讀:[^\)].{,50}?[\)〉]'),
    re.compile(r'延伸閱讀:.{,80}?$'),
    re.compile(r'([◎【]+延伸閱讀[】/].{,100}?)+$'),
    re.compile(r'[・※]'),
    re.compile(r'\($'),
    re.compile(r'\(COVID-19,俗稱武漢肺炎\)'),
    re.compile(r'封面照/.{,20}?提供'),
    re.compile(r'【看更多】.{,200}$'),
    re.compile(r' 詳細講述影片:.{,80}$'),
    re.compile(
        r'(?:(?:《民視新聞網》|請撥打113、110|有話想說嗎\?歡迎來信投稿:|名嘴有說出你的心聲嗎\? 歡迎來信投稿\(全民筆讚\)發表!)\s*)+'
    ),
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


def _get_category(url_pattern):
    try:
        category_word = url_pattern.split('/')[-1][7]
        return CATEGORIES[category_word]
    except Exception:
        # There may not have category.
        return ''


def _get_timestamp(url_pattern):
    try:
        url_datetime = url_pattern.split('/')[-1][:7]
        url_datetime = f'{url_datetime[:4]}{int("0x" + url_datetime[4], 0):02}{url_datetime[5:]}'
        return datetime.strptime(
            url_datetime,
            '%Y%m%d',
        ).timestamp()
    except Exception:
        # There may not have category.
        return 0


def _text_filter(text):
    for text_filter in TEXT_FILTER:
        text = text_filter(string=text)
    return text


def _get_raw_title_article(raw_xml):
    try:
        soup = BeautifulSoup(raw_xml, 'html.parser')
    except Exception:
        raise ValueError('Invalid html format.')

    try:
        title = soup.select('div.col-article > h1.text-center')[0].text
        title = NFKC(title).strip()
    except Exception:
        # FTV response 404 with status code 200.
        # Thus some pages do not have title since it is 404.
        raise ValueError('Fail to find FTV news title.')

    try:
        article_tags = soup.select('div#preface > p, div#newscontent > p')
        article = ' '.join(p_tag.text.strip() for p_tag in article_tags)
        article = NFKC(article).strip()
    except Exception:
        raise ValueError('Fail to find FTV news article.')

    return title, article


def _filter_title(title):
    try:
        for pattern in BAD_TITLE_PATTERNS:
            title = pattern.sub('', title)
    except Exception:
        raise ValueError('Fail to filter FTV news title.')
    return title


def _retrieve_reporter(article):
    try:
        for pattern in REPORTER_PATTERNS:
            match = pattern.search(article)
            if match:
                return article[:match.start()] + article[match.end(
                ):], match.group(1).strip()
        return article, ''
    except Exception:
        # There may not have reporter.
        return article, ''


def _filter_article(article):
    try:
        for pattern in BAD_ARTICLE_PATTERNS:
            article = pattern.sub('', article)
        article = re.sub(r'\s+', ' ', article).strip()

        # If article is not end with period.
        if article and not re.match('[。!?]', article[-1]):
            article = article + '。'
        return article
    except Exception:
        raise ValueError('Fail to filter FTV news article.')


def parser(raw_news: RawNews) -> ParsedNews:
    """Parse FTV news from raw HTML.

    Input news must contain `raw_xml` and `url` since these information cannot
    be retrieved from `raw_xml`.
    """
    # make it easier to test separately

    # 0: extract text from html use bs4 and do character level filter
    title, article = _get_raw_title_article(raw_news.raw_xml)
    title = _text_filter(title)
    article = _text_filter(article)

    # 1: title clean up
    title = _filter_title(title)

    # 2+3: retrieve reporter and cleanup remaining text as article
    article, reporter = _retrieve_reporter(article)
    article = _filter_article(article)

    return ParsedNews(
        url_pattern=raw_news.url_pattern,
        company_id=raw_news.company_id,
        category=_get_category(raw_news.url_pattern),
        timestamp=_get_timestamp(raw_news.url_pattern),
        article=article,
        reporter=reporter,
        title=title,
    )
