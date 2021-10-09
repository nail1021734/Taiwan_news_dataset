from typing import Final

from bs4 import BeautifulSoup

import news.crawlers.util.status_code


def check_ftv_page_exist(url):
    response = news.crawlers.util.request_url.get(url=url)

    soup = BeautifulSoup(response.text, 'html.parser')
    script_tag = soup.select('script')

    # 如果網頁不存在第一個script tag內會有alert這個function，所以回傳False表示網頁不存在。
    return not (script_tag[0].string and script_tag[0].string[:5] == 'alert')


def check_storm_page_exist(url):
    response = news.crawlers.util.request_url.get(url=url)

    soup = BeautifulSoup(response.text, 'html.parser')

    # 若網頁不存在則沒有id為article_title的h1 tag，若select結果為None則回傳False。
    try:
        title = soup.select('h1#article_title')[0].text
        return True
    except Exception as err:
        return False


def get_setn_link(url):
    # setn 新聞不是用 index 暴力爬, 需要先 parse 出每頁新聞的 url, 因此在這裡對
    # 每個 page 進行 parse, 回傳新聞網址.
    response = news.crawlers.util.request_url.get(url=url)

    soup = BeautifulSoup(response.text, 'html.parser')

    news_atag = soup.select('div.newsItems h3.view-li-title > a')

    news_links = [i['href'] for i in news_atag]

    return news_links
