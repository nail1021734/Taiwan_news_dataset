import re


def compress_raw_xml(raw_xml: str):
    return re.sub(r'\s+', ' ', raw_xml)


def compress_url(url: str):
    url_patterns = {
        '中時': 'https://www.chinatimes.com',
        '中央社': 'https://www.cna.com.tw',
        '大紀元': 'https://www.epochtimes.com',
        '東森': 'https://star.ettoday.net',
        '民視': 'https://www.ftvnews.com.tw',
        '自由': 'https://news.ltn.com.tw',
        '新唐人': 'https://www.ntdtv.com',
        '三立': 'https://www.setn.com',
        '風傳媒': 'https://www.storm.mg',
        'tvbs': 'https://news.tvbs.com.tw',
        '聯合報': 'https://udn.com/news',
    }
    for pattern in url_patterns.values():
        if pattern in url:
            url = re.sub(pattern, '', url)
            return url


def company_id(company: str):
    id_table = {
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
    return id_table[company]
