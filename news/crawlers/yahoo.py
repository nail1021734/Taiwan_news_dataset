import json
import os
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def get_links(label):
    i = 0
    links = []
    count = 20
    while True:
        if i > 2000:
            break
        url = f'https://tw.news.yahoo.com/_td-news/api/resource/IndexDataService.getExternalMediaNewsList;count={count};loadMore=true;mrs=%7B%22size%22%3A%7B%22w%22%3A220%2C%22h%22%3A128%7D%7D;newsTab={label[0]};start={i};tag=[{label[1]}];usePrefetch=false?bkt=news-TW-zh-Hant-TW-def&device=desktop&ecma=modern&feature=oathPlayer%2Carticle20%2CvideoDocking&intl=tw&lang=zh-Hant-TW&partner=none&prid=2u6ndb1g8mtd2&region=TW&site=news&tz=Asia%2FTaipei&ver=2.3.1589&returnMeta=true'
        response = requests.get(url)
        try:
            a = json.loads(response.text)
        except:
            continue
        for link in a['data']:
            data_dic = {
                'title': link['title'],
                'company': link['provider_name'],
                'url': 'https://tw.news.yahoo.com' + link['url'],
                'label': label,
                'reporter': link['provider_name']
            }
            links.append(data_dic)
        i += count
    return links

def get_data(links, time_bound):
    result = []
    for link in links:
        url = link['url']
        response = requests.get(url)
        raw_xml = response.text
        soup = BeautifulSoup(raw_xml, 'html.parser')
        try:
            time = soup.find('time')['datetime']
            y = time.split('T')[0].split('-')[0]
            m = time.split('T')[0].split('-')[1]
            d = time.split('T')[0].split('-')[2]
            h = time.split('T')[1].split(':')[0]
            minute = time.split('T')[1].split(':')[1]
            this_time = datetime(year=int(y), month=int(m), day=int(d), hour=int(h), minute=int(minute))
            if this_time < time_bound:
                break
        except:
            time = None
        company = link['company']
        label = link['label']
        reporter = link['reporter']
        title = link['title']
        try:
            article = ''.join([p.text for p in soup.find('div', {'class': 'caas-body'}).find_all('p')])
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
    board = [
        ['entertainment', '"yct%3A001000031"'],
        ['politics', '"yct%3A001000661"'],
        ['world', '"ymedia%3Acategory%3D000000030"%2C"ymedia%3Acategory%3D000000032"'],
        ['society', '"ymedia%3Acategory%3D000000179"%2C"yct%3A001000798"%2C"yct%3A001000667"'],
        ['finance', '"yct%3A001000298"%2C"yct%3A001000123"'],
        ['lifestyle', '"ymedia%3Acategory%3D000000126"%2C"yct%3A001000560"%2C"yct%3A001000374"%2C"yct%3A001001117"%2C"yct%3A001000659"%2C"yct%3A001000616"'],
        ['sports', '"yct%3A001000001"'],
        ['technology', '"yct%3A001000931"%2C"yct%3A001000742"%2C"ymedia%3Acategory%3D000000175"'],
        ['health', '"yct%3A001000395"']
    ]
    for b_name in tqdm(board):
        links = get_links(b_name)
        time_bound = datetime.now() - timedelta(days=1)
        result = get_data(links, time_bound)
        filename = os.path.join('crawlers', 'data', 'yahoo', f'{b_name[0]}_{time_bound.strftime("%Y%m%d")}.json')
        try:
            with open(filename, 'w', encoding='utf8') as input_file:
                json.dump(result, input_file)
        except:
            continue