import json
import os
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def get_links(board):
    result = []
    for page in range(1, 26):
        url = f'https://news.ltn.com.tw/ajax/breakingnews/{board}/{page}'
        try:
            response = requests.get(url)
        except:
            break
        try:
            data = json.loads(response.text)
        except:
            continue
        data = data['data']
        if page != 1:
            data = list(data.values())
        for link in data:
            data_dic = {
                'url': link['url'],
                'time': None,
                'company': '自由時報',
                'label': board,
                'reporter': None,
                'title': link['title'],
                'article': None,
                'raw_xml': None
            }
            result.append(data_dic)
    return result


def get_data(links, time_bound):
    result = []
    for link in links:
        try:
            response = requests.get(link['url'])
            soup = BeautifulSoup(response.text, 'html.parser')
            time = soup.find('span', class_="time").text
            for ap in soup.find_all('p', class_='appE1121'):
                ap.extract()
            for s in soup.find_all('span', class_='ph_d'):
                s.extract()
            for d in soup.find_all('div', {'class': 'photo boxTitle', 'data-desc':'圖片'}):
                d.extract()
            p_tags = soup.find('div', {'class': 'text boxTitle boxText', 'data-desc': '內容頁'}).find_all('p')
            article = ''.join([i.text for i in p_tags])
        except:
            continue
        date = time.strip().split(' ')[0].split('/')
        date = datetime(year=int(date[0]), month=int(date[1]), day=int(date[2]))
        if date < time_bound:
            break
        data_dic = {
            'url': link['url'],
            'time': time.strip(),
            'company': '自由時報',
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
        'society',
        'life',
        'world',
        'local',
        'novelty',
    ]
    for board in tqdm(boards):
        time_bound = datetime.now() - timedelta(days=1)
        links = get_links(board)
        result = get_data(links, time_bound)
        file_path = os.path.join('crawlers', 'data', 'ltn', f'{board}.json')
        json.dump(result, open(file_path, 'w', encoding='utf8'))
