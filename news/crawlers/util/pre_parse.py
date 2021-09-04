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

    # 如果網頁不存在第一個script tag內會有alert這個function，所以回傳False表示網頁不存在。
    return not (script_tag[0].string and script_tag[0].string[:5] == 'alert')


def check_storm_page_exist(url):
    response = requests.get(
        url,
        timeout=news.crawlers.util.status_code.REQUEST_TIMEOUT,
    )
    response.close()

    soup = BeautifulSoup(response.text, 'html.parser')

    # 若網頁不存在則沒有id為article_title的h1 tag，若select結果為None則回傳False。
    try:
        title = soup.select('h1#article_title')[0].text
        return True
    except Exception as err:
        return False


def get_setn_link(url):
    # setn新聞不是用index暴力爬，需要先parse出每頁新聞的url，因此在這裡對
    # 每個page進行parse，回傳新聞網址
    response = requests.get(
        url,
        timeout=news.crawlers.util.status_code.REQUEST_TIMEOUT,
    )
    response.close()

    soup = BeautifulSoup(response.text, 'html.parser')

    news_atag = soup.select('div.newsItems h3.view-li-title > a')

    news_links = [i['href'] for i in news_atag]

    return news_links
