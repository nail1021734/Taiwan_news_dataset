import json
from datetime import date, datetime, timedelta

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def get_links(board, time_bound):
    result = []
    check = False
    for page in range(1, 101):
        url = f'https://www.storm.mg/category/{board[1]}/{page}'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        div_tags = soup.find_all(
            'div', class_='category_card card_thumbs_left')
        for div in div_tags:
            try:
                link = div.find('a', class_='card_link link_title')['href']
            except:
                continue

            try:
                time = div.find('p', class_='card_info right').find(
                    'span', class_='info_time').text
                year = time.split(' ')[0].split('-')[0]
                month = time.split(' ')[0].split('-')[1]
                day = time.split(' ')[0].split('-')[2]
                date = datetime(year=int(year), month=int(month), day=int(day))
                if time_bound >= date:
                    print(date)
                    check = True
                    break
            except:
                time = None
            company = '風傳媒'
            label = board[0]
            try:
                reporter = div.find('span', class_='info_author').text
            except:
                reporter = None

            try:
                title = div.find('a', class_='card_link link_title').find(
                    'h3', class_='card_title').text
            except:
                continue

            data_dic = {
                'url': link,
                'time': time,
                'company': company,
                'label': label,
                'reporter': reporter,
                'title': title,
                'article': None,
                'raw_xml': None
            }
            result.append(data_dic)
        if check:
            break
    return result


def get_data(links):
    result = []
    for link in links:
        url = link['url']
        try:
            response = requests.get(url)
        except:
            continue
        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            p_tags = soup.find('div', id='article_inner_wrapper').find('article').find_all('p')
            article = ''
            for p in p_tags:
                for a in p.find_all('a', {'class': 'notify_wordings'}):
                    a.extract()
                for s in p.find_all('span', {'class': 'related_copy_content'}):
                    s.extract()
                for s in p.find_all('strong'):
                    s.extract()
                article += p.text
        except:
            continue
        raw_xml = response.text
        data_dic = {
            'url': link['url'],
            'time': link['time'],
            'company': link['company'],
            'label': link['label'],
            'reporter': link['reporter'],
            'title': link['title'],
            'article': article,
            'raw_xml': raw_xml
        }
        result.append(data_dic)
    return result


if __name__ == '__main__':
    board = [
        ['政治', 118],
        ['軍事', 26644],
        ['中港澳', 121],
        ['國際', 117],
        ['國內', 22172],
        ['重磅專訪', 171151],
        ['調查', 24667],
        ['風數據', 36948],
        ['運動', 118606],
        ['公民運動', 965],
        ['公共政策', 22168]
    ]
    for b in tqdm(board):
        time_bound = datetime.now() - timedelta(days=1)
        links = get_links(b, time_bound)
        data = get_data(links)
        json.dump(data, open(f'crawlers/data/storm/{b[0]}_{time_bound.strftime("%Y%m%d")}.json', 'w', encoding='utf8'))
