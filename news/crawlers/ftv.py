from collections import Counter
from datetime import datetime, timedelta
from typing import List

import dateutil.parser
import requests
from tqdm import tqdm

import news.crawlers
from news.crawlers.util.normalize import (
    company_id,
    compress_raw_xml,
    compress_url
)
from news.crawlers.db.schema import RawNews

CONTINUE_FAIL_COUNT = 100
COMPANY = '民視'

CATEGORIES = {
    'A': '體育',
    'C': '一般',
    'F': '財經',
    'I': '國際',
    'J': '美食',
    'L': '生活',
    'N': '社會',
    'P': '政治',
    'R': '美食',
    'S': '社會',
    'U': '社會',
    'W': '一般',
}


def get_news_list(
    category: str,
    current_datetime: datetime,
    api: str,
    past_datetime: datetime,
    *,
    debug: bool = False,
) -> List[RawNews]:
    news_list: List[RawNews] = []
    logger = Counter()

    date = current_datetime

    fail_count = 0
    date_str = \
        f'{date.strftime("%Y")}{int(date.strftime("%m")):x}{date.strftime("%d")}'

    if api == 'W':
        iter_range = range(10000)
    else:
        iter_range = range(30)

    # Only show progress bar in debug mode.
    if debug:
        iter_range = tqdm(iter_range)

    for i in iter_range:
        # No more news to crawl.
        if fail_count >= CONTINUE_FAIL_COUNT:
            break

        if api == 'W':
            url = f'https://www.ftvnews.com.tw/news/detail/{date_str}{api}{i:04}'
        else:
            url = f'https://www.ftvnews.com.tw/news/detail/{date_str}{api}{i:02}M1'

        try:
            response = requests.get(
                url,
                timeout=news.crawlers.util.status_code.REQUEST_TIMEOUT,
            )
            response.close()

            # Raise exception if status code is not 200.
            news.crawlers.util.status_code.check_status_code(
                company='ftv',
                response=response
            )
            # Check if page exist.
            if not news.crawlers.util.pre_parse.check_ftv_page_exist(url):
                continue

            # If `status_code == 200` and successfully parsed (only happend when
            # such news is not missing), reset `fail_count`.
            fail_count = 0

            news_list.append(RawNews(
                company_id=company_id(COMPANY),
                raw_xml=compress_raw_xml(response.text),
                url_pattern=compress_url(url),
            ))
        except Exception as err:
            fail_count += 1

            if err.args:
                logger.update([err.args[0]])
            continue

    # Only show error stats in debug mode.
    if debug:
        for k, v in logger.items():
            print(f'{k}: {v}')

    return news_list


def main(
    current_datetime: datetime,
    db_name: str,
    past_datetime: datetime,
    *,
    debug: bool = False,
):
    if past_datetime > current_datetime:
        raise ValueError('Must have `past_datetime <= current_datetime`.')

    # Get database connection.
    conn = news.crawlers.db.util.get_conn(db_name=f'{db_name}')
    cur = conn.cursor()
    news.crawlers.db.create.create_table(cur=cur)

    for api, category in CATEGORIES.items():
        date = current_datetime
        # Commit database once a day.
        while date >= past_datetime:
            news.crawlers.db.write.write_new_records(
                cur=cur,
                news_list=get_news_list(
                    category=category,
                    current_datetime=date,
                    api=api,
                    debug=debug,
                    past_datetime=date - timedelta(days=1),
                ),
            )

            # Go back 1 day.
            date = date - timedelta(days=1)

            conn.commit()

    # Close database connection.
    conn.close()
