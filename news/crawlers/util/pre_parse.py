import requests
from bs4 import BeautifulSoup

import news.crawlers


def check_ftv_page_exist(url):
    response = requests.get(
        url,
        timeout=news.crawlers.util.status_code.REQUEST_TIMEOUT,
    )
    response.close()

    soup = BeautifulSoup(response.text, 'html.parser')
    script_tag = soup.select('script')

    if script_tag[0].string and script_tag[0].string[:5] == 'alert':
        return False
    return True


def check_storm_page_exist(url):
    response = requests.get(
        url,
        timeout=news.crawlers.util.status_code.REQUEST_TIMEOUT,
    )
    response.close()

    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        title = soup.select('h1#article_title')[0].text
        return True
    except Exception as err:
        return False
