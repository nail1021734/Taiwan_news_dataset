import re

COMPANY_URL = {
    '中時': 'https://www.chinatimes.com/',
    '中央社': 'https://www.cna.com.tw/',
    '大紀元': 'https://www.epochtimes.com/',
    '東森': 'https://star.ettoday.net/',
    '民視': 'https://www.ftvnews.com.tw/',
    '自由': 'https://news.ltn.com.tw/',
    '新唐人': 'https://www.ntdtv.com/',
    '三立': 'https://www.setn.com/',
    '風傳媒': 'https://www.storm.mg/',
    'tvbs': 'https://news.tvbs.com.tw/',
    '聯合報': 'https://udn.com/news/',
}

URL_PATTERNS = {
    '中時': re.compile(r'https://www\.chinatimes\.com/'),
    '中央社': re.compile(r'https://www\.cna\.com\.tw/'),
    '大紀元': re.compile(r'https://www\.epochtimes\.com/'),
    '東森': re.compile(r'https://star\.ettoday\.net/'),
    '民視': re.compile(r'https://www\.ftvnews\.com\.tw/'),
    '自由': re.compile(r'https://news\.ltn\.com\.tw/'),
    '新唐人': re.compile(r'https://www\.ntdtv\.com/'),
    '三立': re.compile(r'https://www\.setn\.com/'),
    '風傳媒': re.compile(r'https://www\.storm\.mg/'),
    'tvbs': re.compile(r'https://news\.tvbs\.com\.tw/'),
    '聯合報': re.compile(r'https://udn\.com/news/'),
}

COMPANY_ID_TABLE = {
    '中時': 1,
    '中央社': 2,
    '大紀元': 3,
    '東森': 4,
    '民視': 5,
    '自由': 6,
    '新唐人': 7,
    '三立': 8,
    '風傳媒': 9,
    'tvbs': 10,
    '聯合報': 11,
}

WHITESPACE_COLLAPSE = re.compile(r'\s+')


def compress_raw_xml(raw_xml: str):
    r"""將 `raw_xml` 中多個空白合成一個空白"""
    return WHITESPACE_COLLAPSE.sub(' ', raw_xml)


def compress_url(url: str, company: str):
    r"""去掉同一新聞媒體中 url 相同的部份"""
    return URL_PATTERNS[company].sub('', url)


def company_id(company: str):
    r"""將每個媒體用 ID 表示, 取代文字"""
    return COMPANY_ID_TABLE[company]
