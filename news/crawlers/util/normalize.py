import re
from typing import Dict, List

####################################################
#                     WARNING
# NEW news company must be appended at the end.
# COMPANT_ID cannot repeat.
####################################################
COMPANY_ID_LOOKUP_TABLE: Dict[str, int] = {
    '中時': 0,
    '中央社': 1,
    '大紀元': 2,
    '東森': 3,
    '民視': 4,
    '自由': 5,
    '新唐人': 6,
    '三立': 7,
    '風傳媒': 8,
    'tvbs': 9,
    '聯合報': 10,
}

COMPANY_URL_LOOKUP_TABLE: Dict[int, str] = {
    COMPANY_ID_LOOKUP_TABLE['中時']:
        r'https://www.chinatimes.com/',
    COMPANY_ID_LOOKUP_TABLE['中央社']:
        r'https://www.cna.com.tw/news/aipl/',
    COMPANY_ID_LOOKUP_TABLE['大紀元']:
        r'https://www.epochtimes.com/b5/',
    COMPANY_ID_LOOKUP_TABLE['東森']:
        r'https://star.ettoday.net/news/',
    COMPANY_ID_LOOKUP_TABLE['民視']:
        r'https://www.ftvnews.com.tw/news/detail/',
    COMPANY_ID_LOOKUP_TABLE['自由']:
        r'https://news.ltn.com.tw/ajax/breakingnews/',
    COMPANY_ID_LOOKUP_TABLE['新唐人']:
        r'https://www.ntdtv.com/b5/',
    COMPANY_ID_LOOKUP_TABLE['三立']:
        r'https://www.setn.com/',
    COMPANY_ID_LOOKUP_TABLE['風傳媒']:
        r'https://www.storm.mg/article/',
    COMPANY_ID_LOOKUP_TABLE['tvbs']:
        r'https://news.tvbs.com.tw/',
    COMPANY_ID_LOOKUP_TABLE['聯合報']:
        r'https://udn.com/',
}

# List lookup with index is O(1).
COMPANY_URL_FASTEST_LOOKUP_TABLE: List[str] = [
    COMPANY_URL_LOOKUP_TABLE[company_id]
    for company_id in sorted(COMPANY_ID_LOOKUP_TABLE.values())
]

COMPRESS_URL_PATTERN_LOOKUP_TABLE: Dict[int, re.Pattern] = {
    COMPANY_ID_LOOKUP_TABLE['中時']:
        re.compile(
            r'https://www.chinatimes.com/([rn])'
            + r'(?:ealtimenews|ewspapers)/(\d+)-(\d+)',
        ),
    COMPANY_ID_LOOKUP_TABLE['中央社']:
        re.compile(
            r'https://www.cna.com.tw/news/aipl/(\d+)\.aspx',
        ),
    COMPANY_ID_LOOKUP_TABLE['大紀元']:
        re.compile(
            r'https://www.epochtimes.com/b5/(\d+)/(\d+)/(\d+)/n(\d+)\.htm',
        ),
    COMPANY_ID_LOOKUP_TABLE['東森']:
        re.compile(
            r'https://star.ettoday.net/news/(\d+)',
        ),
    COMPANY_ID_LOOKUP_TABLE['民視']:
        re.compile(
            r'https://www.ftvnews.com.tw/news/detail/(.+)',
        ),
    COMPANY_ID_LOOKUP_TABLE['自由']:
        re.compile(
            r'https://news.ltn.com.tw/news/(\w+)/breakingnews/(\d+)',
        ),
    COMPANY_ID_LOOKUP_TABLE['新唐人']:
        re.compile(
            r'https://www.ntdtv.com/b5/(\d+)/(\d+)/(\d+)/a(\d+)\.html',
        ),
    COMPANY_ID_LOOKUP_TABLE['三立']:
        re.compile(
            r'https://www.setn.com/News.aspx\?.*NewsID=(\d+)',
        ),
    COMPANY_ID_LOOKUP_TABLE['風傳媒']:
        re.compile(
            r'https://www.storm.mg/article/(\d+)\?mode=whole',
        ),
    COMPANY_ID_LOOKUP_TABLE['tvbs']:
        re.compile(
            r'https://news.tvbs.com.tw/(\w+)/(\d+)',
        ),
    COMPANY_ID_LOOKUP_TABLE['聯合報']:
        re.compile(
            r'https://udn.com/news/story/(\d+)/(\d+)',
        ),
}

# List lookup with index is O(1).
COMPRESS_URL_PATTERN_FASTEST_LOOKUP_TABLE: List[re.Pattern] = [
    COMPRESS_URL_PATTERN_LOOKUP_TABLE[company_id]
    for company_id in sorted(COMPANY_ID_LOOKUP_TABLE.values())
]

WHITESPACE_COLLAPSE_PATTERN: re.Pattern = re.compile(r'\s+')


def compress_raw_xml(raw_xml: str) -> str:
    r"""將 `raw_xml` 中的多餘資訊去除.

    去除資訊包含:
    - 多個空白合成一個空白.
    - 開頭與結尾的空白.
    """
    return WHITESPACE_COLLAPSE_PATTERN.sub(' ', raw_xml).strip()


def compress_url(company_id: int, url: str) -> str:
    r"""去掉同一新聞媒體中 url 相同的部份."""
    match = COMPRESS_URL_PATTERN_FASTEST_LOOKUP_TABLE[company_id].match(url)
    if not match:
        return url
    return '-'.join(match.groups())


def get_company_id(company: str) -> int:
    r"""取得每個新聞媒體所對應到的流水號.

    使用流水號取代文字的目的為加速計算與節省儲存空間.
    """
    return COMPANY_ID_LOOKUP_TABLE[company]


def get_company_url(company_id: int) -> str:
    r"""取得每個新聞媒體網站的 domain name."""
    return COMPANY_URL_FASTEST_LOOKUP_TABLE[company_id]
