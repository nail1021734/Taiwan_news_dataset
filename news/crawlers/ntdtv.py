import json
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def get_links(board, start_page, end_page):
    result = []
    for i in range(start_page, end_page):
        url = f'https://www.ntdtv.com/b5/prog{board[1]}/{i}'
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
        except:
            break
        try:
            all_post = soup.find('div', class_='post_list').find_all('div', class_='one_post')
        except:
            continue
        for post in all_post:
            try:
                title_a = post.find('div', class_='title').find('a')
            except:
                continue
            data_dic = {
                'url': title_a['href'],
                'time': None,
                'company': '新唐人',
                'label': board[0],
                'reporter': None,
                'title': title_a.text,
                'article': None,
                'raw_xml': None
            }
            # print(data_dic)
            result.append(data_dic)
    return result

def get_data(link, time_bound):
    result = []
    for link in tqdm(links):
        url = link['url']
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            time = soup.find('div', class_='article_info').find('div', class_='time').find('span').text
        except:
            time = None
        date = time.split(' ')[0].split('-')
        date = datetime(year=int(date[0]), month=int(date[1]), day=int(date[2]))
        if date < time_bound:
            break
        try:
            article = ''.join([i.text for i in soup.find('div', class_='article_content').find('div', class_='post_content').find_all('p')])
        except:
            continue
        data_dic = {
            'url': url,
            'time': time,
            'company': '新唐人',
            'label': link['label'],
            'reporter': None,
            'title': link['title'],
            'article': article,
            'raw_xml': response.text
        }
        result.append(data_dic)
    return result

if __name__ == "__main__":
    board = [
        ['國際', 202],
        ['港澳', 205],
        ['財經', 208],
        ['健康', 1255],
        ['體育', 211],
        ['美國', 203],
        ['大陸', 204]
    ]
    for b in tqdm(board):
        for page in tqdm(range(1, 501, 50)):
            time_bound = datetime.now() - timedelta(days=1)
            links = get_links(b, page, page+50)
            data = get_data(links, time_bound)
            json.dump(data, open(f'crawlers/data/ntdtv/{b[0]}_p{page}-p{page+50}_{time_bound.strftime("%Y%m%d")}.json', 'w', encoding='utf8'))