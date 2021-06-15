from collections import Counter
from datetime import datetime, timedelta
from typing import List

import requests
from tqdm import tqdm

import news.crawlers
import news.db
from news.db.schema import News

CONTINUE_FAIL_COUNT = 5000


def get_news_list(
    category: str,
    current_datetime: datetime,
    api: str,
    past_datetime: datetime,
    *,
    debug: bool = False,
):
    news_list: List[News] = []
    fail_count = 0
    logger = Counter()

    date = current_datetime

    while date > past_datetime:
        date_str = date.strftime('%Y%m%d')

        # Only show progress bar in debug mode.
        iter_range = range(100000)
        if debug:
            iter_range = tqdm(iter_range)

        for i in iter_range:
            # No more news to crawl.
            if fail_count >= CONTINUE_FAIL_COUNT:
                fail_count = 0
                break

            url = f'https://www.chinatimes.com/realtimenews/{date_str}{i:06d}-{api}?chdtv'
            response = requests.get(url)

            # Got banned.
            if response.status_code == 403:
                logger.update(['Got banned.'])
                news.crawlers.util.after_banned_sleep()
                fail_count += 1
                continue

            # Some id is not matched.
            if response.status_code == 404:
                logger.update(['News not found.'])
                fail_count += 1
                continue

            # Something weird happend.
            if response.status_code != 200:
                logger.update(['Weird.'])
                fail_count += 1
                continue

            # If `status_code == 200`, reset `fail_count`.
            fail_count = 0

            try:
                parsed_news = news.preprocess.chinatimes.parse(ori_news=News(
                    raw_xml=response.text,
                    url=url,
                ))
            except Exception as err:
                # Skip parsing if error.
                if err.args:
                    logger.update([err.args[0]])
                continue

            news_list.append(parsed_news)

            # Sleep to avoid banned.
            news.crawlers.util.before_banned_sleep()

        date = date - timedelta(days=1)

    # Only show error stats in debug mode.
    if debug:
        for k, v in logger.items():
            print(f'{k}: {v}')

    return news_list

    # # Only first 10 pages have content.
    # for i in range(10):
    #     url = f'https://www.chinatimes.com/{api}/total?page={i+1}&chdtv'
    #     soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    #     section_tag = soup.find('section', class_='article-list')
    #     ul_tag = section_tag.find('ul', class_='vertical-list list-style-none')
    #     li_tags = ul_tag.find_all('li')
    #     for li_tag in li_tags:
    #         div_tag = li_tag.find('div', class_='col')
    #         datetime_tag = div_tag.find('div', class_='meta-info').find('time')
    #         h3_tag = div_tag.find('h3', class_='title')
    #         a_tag = h3_tag.find('a')
    #         news_date = datetime_tag['datetime'].split(' ')[0].split('-')
    #         news_time = datetime_tag['datetime'].split(' ')[1].split(':')
    #         news_datetime = datetime(
    #             year=int(news_date[0]),
    #             month=int(news_date[1]),
    #             day=int(news_date[2]),
    #             hour=int(news_time[0]),
    #             minute=int(news_time[1]),
    #         )
    #         # Convert to UTC.
    #         news_datetime = datetime.utcfromtimestamp(
    #             news_datetime.timestamp()
    #         ).replace(tzinfo=timezone.utc)

    #         # Only consider news which datetime is within `datetime_bound`.
    #         if news_datetime < datetime_bound:
    #             break

    #         # News url.
    #         news_url = 'https://www.chinatimes.com' + a_tag['href']

    #         # Raw html.
    #         raw_xml = requests.get(news_url).text
    #         raw_xml = re.sub(r'\s+', ' ', raw_xml)

    #         news_list.append(News(
    #             category=category,
    #             company='中時',
    #             datetime=news_datetime.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
    #             raw_xml=raw_xml,
    #             title=a_tag.text,
    #             url=news_url,
    #         ))

    return news_list


def main(
    current_datetime: datetime,
    db_name: str,
    past_datetime: datetime,
    *,
    debug: bool = False,
):
    # categories = {
    #     '政治': 'politic',
    #     '言論': 'opinion',
    #     '生活': 'life',
    #     '娛樂': 'star',
    #     '財經': 'money',
    #     '國際': 'world',
    #     '兩岸': 'chinese',
    #     '社會': 'society',
    #     '軍事': 'armament',
    #     '科技': 'technologynews',
    #     '體育': 'sports',
    #     '網推': 'hottopic',
    #     '健康': 'health',
    #     '運勢': 'fortune',
    #     '寶島': 'taiwan',
    # }
    categories = {
        '政治': '260407',
        '中時社論': '262101',
        '旺報社評': '262102',
        '工商社論': '262113',
        '快評': '262103',
        '時論廣場': '262104',
        '尚青論壇': '262114',
        '兩岸徵文': '262106',
        '兩岸史話': '262107',
        '海納百川': '262110',
        '玩食': '260405',
        '消費': '260113',
        '時尚': '260405',
        '新消息': '262301',
        '華人星光': '262404',
        '哈燒日韓、西洋熱門': '260404',
        '財經': '260410',
        '國際': '260408',
        '兩岸': '260409',
        '社會': '260402',
        '軍事': '260417',
        '科技': '260412',
        '高爾夫': '260111',
        '球類': '260403',
        '萌寵': '260819',
        '搜奇': '260809',
        '歷史': '260812',
        '健康': '260418',
        '時人真話': '260102',
        '運勢': '260423',
        '寶島': '260421'
    }

    # Get database connection.
    conn = news.db.util.get_conn(db_name=db_name)
    cur = conn.cursor()
    news.db.create.create_table(cur=cur)

    for category, api in categories.items():
        news.db.write.write_new_records(
            cur=cur,
            news_list=get_news_list(
                api=api,
                category=category,
                current_datetime=current_datetime,
                debug=debug,
                past_datetime=past_datetime,
            ),
        )

        conn.commit()

    # Close database connection.
    conn.close()
