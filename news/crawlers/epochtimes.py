import json
import os
from datetime import date, datetime, timedelta

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def get_links(board, start, end):
    result = []
    for page in range(start, end):
        url = f'https://www.epochtimes.com/b5/{board[1]}_{page}.htm'
        try:
            response = requests.get(url)
        except:
            break
        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            div = soup.find('div', class_='post_list left_col').find_all(
                'div', class_='one_post')
        except:
            continue
        for link in div:
            try:
                url = link.find('div', class_='title').find('a')['href']
                title = link.find('div', class_='title').find('a').text
            except:
                continue
            data_dic = {
                'url': url,
                'time': None,
                'company': '大紀元',
                'label': board[0],
                'reporter': None,
                'title': title,
                'article': None,
                'raw_xml': None
            }
            result.append(data_dic)
    return result


def get_data(links, time_bound):
    result = []
    for link in links:
        url = link['url']
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            time = soup.find('div', class_='info').find('time')['datetime']
            article = ''.join([i.text for i in soup.find('div', {
                            'itemprop': 'articleBody', 'class': 'post_content', 'id': 'artbody'}).find_all('p')])
        except:
            continue
        date = time.split('T')[0].split('-')
        date = datetime(year=int(date[0]), month=int(date[1]), day=int(date[2]))
        if date < time_bound:
            break
        data_dic = {
            'url': url,
            'time': time,
            'company': '大紀元',
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
        ['大陸', 'nsc413'],
        ['美國', 'nsc412'],
        ['香港', 'ncid1349362'],
        ['國際', 'nsc418'],
        ['台灣', 'ncid1349361'],
        ['科技', 'nsc419'],
        ['財經', 'nsc420']
    ]
    for board in tqdm(boards):
        interval = 50
        for page in range(2, 800, interval):
            time_bound = datetime.now() - timedelta(days=1)
            links = get_links(board, page, page+interval)
            data = get_data(links, time_bound)
            if data == []:
                break
            file_path = os.path.join(
                'crawlers', 'data', 'epochtimes', f'{board[0]}_{page}_{time_bound.strftime("%Y%m%d")}.json')
            json.dump(data, open(file_path, 'w', encoding='utf8'))
