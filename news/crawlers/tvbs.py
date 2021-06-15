import json
import os
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def get_links(board, nowdate, timebound):
    result = []
    day_delta = timedelta(days=1)
    while nowdate > timebound:
        url_date = f'{nowdate.year}-{nowdate.month:02}-{nowdate.day:02}'
        url = f'https://news.tvbs.com.tw/realtime/{board}/{url_date}'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find('main').find('div', class_='list').find_all('li')
        for link in links:
            try:
                url = 'https://news.tvbs.com.tw' + link.find('a')['href']
                title = link.find('h2').text
            except:
                continue
            data_dic = {
                'url': url,
                'time': None,
                'company': 'TVBS',
                'label': board,
                'reporter': None,
                'title': title,
                'article': None,
                'raw_xml': None
            }
            result.append(data_dic)
        nowdate -= day_delta
    return result

def get_data(links):
    result = []
    for link in links:
        url = link['url']
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
        except:
            continue
        try:
            time = soup.find('main').find('div', class_='author_box').find('div', class_='author').text
            time = time.split()[-2].split('：')[1] + ' ' + time.split()[-1]
        except:
            time = None
        try:
            article = soup.find('main').find('div', {'itemprop':'articleBody'}).find('div', {'id': 'news_detail_div', 'class': 'article_content'})
            for s in article.find_all('span', class_='font_color5 text_center img_small'):
                s.extract()
            for s in article.find_all('br'):
                s.extract()
            for s in article.find_all('div'):
                s.extract()
            article = article.text
        except:
            continue
        data_dic = {
            'url': url,
            'time': time,
            'company': 'TVBS',
            'label': link['label'],
            'reporter': None,
            'title': link['title'],
            'article': article,
            'raw_xml': response.text
        }
        result.append(data_dic)
    return result

if __name__ == '__main__':
    boards = [
        'politics',
        'local',
        'world',
        'china',
        'life',
        'health',
        'tech',
        'sports'
    ]

    for board in tqdm(boards):
        now_date = datetime.now()
        time_bound = datetime.now() - timedelta(days=1)
        links = get_links(board, nowdate=now_date, timebound=time_bound)
        data = get_data(links)
        json.dump(data, open(f'crawlers/data/TVBS/{board}_{time_bound.strftime("%Y%m%d")}.json', 'w', encoding='utf8'))