import json
import os
from datetime import date, datetime, timedelta

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def get_links(page_group_id):
    result = []
    for i in range(20):
        url = f"https://www.setn.com/ViewAll.aspx?PageGroupID={page_group_id}&p={i+1}"
        raw_xml = requests.get(url)
        soup = BeautifulSoup(raw_xml.text, 'html.parser')
        div_tags = soup.find_all('div', class_='col-sm-12 newsItems')
        for tag in div_tags:
            temp = tag.find_all('a')
            result.append(
                {
                    'label': temp[0].text,
                    'link': temp[1]['href']
                }
            )

    return result


def get_data(links_dict, last_time):
    result = []
    base_url = "https://www.setn.com"

    for news in links_dict:
        url = f'{base_url}{news["link"]}'
        try:
            raw_xml = requests.get(url)
        except:
            continue
        try:
            soup = BeautifulSoup(raw_xml.text, 'html.parser')
        except:
            continue

        try:
            reporter = soup.find('article').find('p').text.split('／')[0][2:]
        except:
            reporter = None

        try:
            title = soup.find('h1', class_="news-title-3").text
        except:
            title = None

        try:
            label = news['label']
            company = '三立'
            for p in soup.find_all('p', {'style': 'text-align: center;'}):
                p.extract()
            for p in soup.find_all('p', {'style': 'text-align:center'}):
                p.extract()
            p_tags = soup.find('article').find_all('p')[1:]
            article = ''.join([i.text for i in p_tags])
        except:
            continue

        try:
            time = soup.find('time', class_='page-date').text
            y = time.split(' ')[0].split('/')[0]
            m = time.split(' ')[0].split('/')[1]
            d = time.split(' ')[0].split('/')[2]
            this_date = datetime(year=int(y), month=int(m), day=int(d))
            if last_time > this_date:
                break
        except:
            time = None

        result.append(
            {
                'url': url,
                'time': time,
                'company': company,
                'label': label,
                'reporter': reporter,
                'title': title,
                'article': article,
                'raw_xml': raw_xml.text
            }
        )

    return result


if __name__ == "__main__":
    group_id = {
        '政治': 6,
        '社會': 41,
        '國際': 5,
        '生活': 4,
        '健康': 65,
        '運動': 34,
        '汽車': 12,
        '地方': 97,
        '名家': 9,
        '新奇': 42,
        '科技': 7,
        '財經': 2,
        '寵物': 47
    }
    data_path = os.path.join('crawlers', 'data', 'setn')
    for file_name, _id in tqdm(list(group_id.items())):
        links = get_links(page_group_id=_id)
        time_bound = datetime.now() - timedelta(days=1)
        result = get_data(links, time_bound)
        file_path = os.path.join(data_path, f'{file_name}.json')
        with open(file_path, 'w', encoding='utf8') as output_file:
            json.dump(result, output_file)
