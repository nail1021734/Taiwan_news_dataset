import re


def compress_raw_xml(raw_xml: str):
    return re.sub(r'\s+', ' ', raw_xml)


def compress_url(url: str):
    url_patterns = {
        '中時': 'https://www.chinatimes.com',
        '中央社': 'https://www.cna.com.tw',
        '大紀元': 'https://www.epochtimes.com',
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
    }
    return id_table[company]
