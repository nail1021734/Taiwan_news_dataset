import json
import os
import random
import time
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def get_links(start_index, end_index, last_time):
    links = []
    time_check = 0
    for i in range(start_index, end_index):
        url = f"https://udn.com/api/more?page={i}&id=&channelId=1&cate_id=99&type=breaknews&totalRecNo=9654"
        response = requests.get(url)
        tmp_datas = json.loads(response.text)
        tmp_datas = tmp_datas['lists']
        for link in tmp_datas:
            data_dic = {
                'url': f'https://udn.com{link["titleLink"]}',
                'time': link['time']['date'],
                'company': '聯合',
                'label': None,
                'reporter': None,
                'title': link['title'],
                'article': None,
                'raw_xml': None
            }
            y = data_dic['time'].split(' ')[0].split('-')[0]
            m = data_dic['time'].split(' ')[0].split('-')[1]
            d = data_dic['time'].split(' ')[0].split('-')[2]
            this_time = datetime(year=int(y), month=int(m), day=int(d))
            if last_time > this_time:
                time_check = 1
                break
            links.append(data_dic)
        if time_check == 1:
            break

    return links

def get_data(links):
    result = []
    for link_dic in links:
        url = link_dic['url']
        response = requests.get(url)
        raw_xml = response.text
        soup = BeautifulSoup(raw_xml, 'html.parser')

        time = link_dic['time']
        title = link_dic['title']
        company = link_dic['company']

        try:
            label = soup.find('section', class_='article-content__info').find_all('a')[1].text
        except:
            label = None
        try:
            reporter = soup.find('span', class_='article-content__author').find('a').text
        except:
            reporter = None
        try:
            article = ''.join([i.text for i in soup.find('article', class_='article-content').find_all('p')])
        except:
            continue

        data_dic = {
            'url': url,
            'time': time,
            'company': company,
            'label': label,
            'reporter': reporter,
            'title': title,
            'article': article,
            'raw_xml': raw_xml
        }
        result.append(data_dic)

    return result

if __name__ == "__main__":
    interval = 100
    save_path = os.path.join('crawlers', 'data', 'uni')
    for i in tqdm(range(1, 461, interval)):
        time_bound = datetime.now() - timedelta(days=1)
        filename = time_bound.strftime('%Y%m%d') + '.json'
        file_path = os.path.join(save_path, filename)
        links = get_links(i, i + interval, last_time=time_bound)
        result = get_data(links)
        with open(file_path, 'w', encoding='utf8') as output_file:
            json.dump(result, output_file)
        break

