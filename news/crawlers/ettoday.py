import json
import os
from datetime import datetime, timedelta
from time import sleep

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def get_links(time_bound):
    now_date = datetime.now()
    url = 'https://www.ettoday.net/show_roll.php'
    while now_date > time_bound:
        result = []
        print(now_date)
        for offset in tqdm(range(1, 151)):
            data_date = f'{now_date.year}{now_date.month:02}{now_date.day:02}.xml'
            data = {'offset': offset, 'tPage': 3, 'tFile': data_date, 'tOt': 0, 'tSi': 100, 'tAr': 0}
            response = requests.post(url, data=data)
            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.find_all('h3'):
                try:
                    time = link.find('span', class_='date').text
                    label = link.find('em').text
                    title = link.find('a').text
                except:
                    continue
                data_dic = {
                    'url': 'https://www.ettoday.net' + link.find('a')['href'],
                    'time': time,
                    'company': 'ettoday',
                    'label': label,
                    'reporter': None,
                    'title': title,
                    'article': None,
                    'raw_xml': None
                }
                result.append(data_dic)
        filename = f'{now_date.year}{now_date.month:02}{now_date.day:02}'
        last_time = result[-1]['time'].split(' ')[0].split('/')
        now_date = datetime(year=int(last_time[0]), month=int(last_time[1]), day=int(last_time[2]))
        data = get_data(result)
        json.dump(data, open(f'crawlers/data/ettoday/{filename}.json', 'w', encoding='utf8'))

def get_data(links):
    result = []
    for link in tqdm(links):
        url = link['url']
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            p_tags = soup.find('article').find('div', {'class': 'story', 'itemprop': 'articleBody'}).find_all('p')
            article = ""
            for p in p_tags:
                for s in p.find_all('span'):
                    s.extract()
                for s in p.find_all('strong'):
                    s.extract()
                article += p.text
        except:
            continue
        data_dic = {
            'url': url,
            'time': link['time'],
            'company': 'ettoday',
            'label': link['label'],
            'reporter': None,
            'title': link['title'],
            'article': article,
            'raw_xml': response.text
        }
        result.append(data_dic)
    return result

if __name__ == '__main__':
    time_bound = datetime.now() - timedelta(days=1)
    get_links(time_bound)