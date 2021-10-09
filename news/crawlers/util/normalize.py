import re
from typing import Dict, Final, List

####################################################
#                     WARNING
# NEW news company must be appended at the end.
# COMPANT_ID cannot repeat.
####################################################
COMPANY_ID_LOOKUP_TABLE: Final[Dict[str, int]] = {
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

COMPANY_URL_LOOKUP_TABLE: Final[Dict[int, str]] = {
    COMPANY_ID_LOOKUP_TABLE['中時']: r'https://www.chinatimes.com/realtimenews/',
    COMPANY_ID_LOOKUP_TABLE['中央社']: r'https://www.cna.com.tw/',
    COMPANY_ID_LOOKUP_TABLE['大紀元']: r'https://www.epochtimes.com/',
    COMPANY_ID_LOOKUP_TABLE['東森']: r'https://star.ettoday.net/',
    COMPANY_ID_LOOKUP_TABLE['民視']: r'https://www.ftvnews.com.tw/',
    COMPANY_ID_LOOKUP_TABLE['自由']: r'https://news.ltn.com.tw/',
    COMPANY_ID_LOOKUP_TABLE['新唐人']: r'https://www.ntdtv.com/',
    COMPANY_ID_LOOKUP_TABLE['三立']: r'https://www.setn.com/',
    COMPANY_ID_LOOKUP_TABLE['風傳媒']: r'https://www.storm.mg/',
    COMPANY_ID_LOOKUP_TABLE['tvbs']: r'https://news.tvbs.com.tw/',
    COMPANY_ID_LOOKUP_TABLE['聯合報']: r'https://udn.com/news/',
}

# List lookup with index is O(1).
COMPANY_URL_FASTEST_LOOKUP_TABLE: Final[List[str]] = [
    COMPANY_URL_LOOKUP_TABLE[company_id]
    for company_id in sorted(COMPANY_ID_LOOKUP_TABLE.values())
]

# List lookup with index is O(1).
URL_PATTERN_FASTEST_LOOKUP_TABLE: Final[List[re.Pattern]] = [
    re.compile(url)
    for url in COMPANY_URL_FASTEST_LOOKUP_TABLE
]

WHITESPACE_COLLAPSE_PATTERN: Final[re.Pattern] = re.compile(r'\s+')


def compress_raw_xml(raw_xml: Final[str]) -> str:
    r"""將 `raw_xml` 中的多餘資訊去除.

    去除資訊包含:
    - 多個空白合成一個空白.
    - 開頭與結尾的空白.
    """
    return WHITESPACE_COLLAPSE_PATTERN.sub(' ', raw_xml).strip()


def compress_url(company_id: Final[int], url: Final[str]) -> str:
    r"""去掉同一新聞媒體中 url 相同的部份."""
    return URL_PATTERN_FASTEST_LOOKUP_TABLE[company_id].sub('', url)


def get_company_id(company: Final[str]) -> int:
    r"""取得每個新聞媒體所對應到的流水號.

    使用流水號取代文字的目的為加速計算與節省儲存空間.
    """
    return COMPANY_ID_LOOKUP_TABLE[company]


def get_company_url(company_id: Final[int]) -> str:
    r"""取得每個新聞媒體網站的 domain name."""
    return COMPANY_URL_FASTEST_LOOKUP_TABLE[company_id]
