import os
import re
from datetime import datetime, timedelta, timezone
from typing import List

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

import news.db
from news.db.schema import News

CONTINUE_FAIL_COUNT = 50


def get_news_list(datetime_bound: datetime, debug: bool = False):
    news_list: List[News] = []

    cur_datetime = datetime.now(timezone.utc)

    fail_count = 0
    while cur_datetime > datetime_bound:
        # Only show progress bar in debug mode.
        iter_range = range(10000)
        if debug:
            iter_range = tqdm(iter_range)

        for i in iter_range:
            news_date = datetime.strftime(cur_datetime, '%Y%m%d')

            url = f'https://www.cna.com.tw/news/aipl/{news_date}{i:04d}.aspx'
            response = requests.get(url)

            # Missing news or no news.
            if response.status_code != 200:
                fail_count += 1
            # News is available.
            else:
                # Raw html.
                raw_xml = response.text
                raw_xml = re.sub(r'\s+', ' ', raw_xml)

                soup = BeautifulSoup(raw_xml, 'html.parser')
                category = (
                    soup.find('div', class_='breadcrumb')
                    .find_all('a')[-1].text
                )
                content_tag = (
                    soup.find('article', class_='article')
                    .find('div', class_='centralContent')
                )
                # Retrieve publish time and convert to UTC.
                news_datetime = (
                    content_tag.find('div', class_='timeBox')
                    .find('div', class_='updatetime').find('span').text
                )
                news_datetime = datetime.strptime(
                    news_datetime,
                    '%Y/%m/%d %H:%M',
                )
                news_datetime = datetime.utcfromtimestamp(
                    news_datetime.timestamp()
                )
                title = content_tag.find('h1').find('span').text
                article = ' '.join(
                    map(lambda p_tag: p_tag.text, content_tag.find_all('p'))
                )

                news_list.append(News(
                    article=article,
                    category=category,
                    company='中央社',
                    datetime=news_datetime.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                    raw_xml=raw_xml,
                    title=title,
                    url=url,
                ))
                fail_count = 0

            # No more news to crawl.
            if fail_count >= CONTINUE_FAIL_COUNT:
                break

        # Go back 1 day.
        cur_datetime = cur_datetime - timedelta(days=1)
        fail_count = 0

    return news_list


def main(db_name: str, debug: bool = False):
    # Get database connection.
    conn = news.db.util.get_conn(db_name=db_name)
    cur = conn.cursor()
    news.db.create.create_table(cur=cur)

    # Only consider news in past 2 days.
    datetime_bound = datetime.now(timezone.utc) - timedelta(days=2)

    news.db.write.write_new_records(
        cur=cur,
        news_list=get_news_list(
            datetime_bound=datetime_bound,
            debug=debug,
        ),
    )

    conn.commit()

    # Close database connection.
    conn.close()
