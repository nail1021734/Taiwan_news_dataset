from collections import Counter
from datetime import datetime, timedelta
from typing import List

import dateutil.parser
import requests
from tqdm import tqdm

import news.crawlers
import news.db
from news.db.schema import News

CONTINUE_FAIL_COUNT = 100


def get_news_list(
    current_datetime: datetime,
    past_datetime: datetime,
    *,
    debug: bool = False,
):
    news_list: List[News] = []
    logger = Counter()

    date = current_datetime

    while date > past_datetime:
        fail_count = 0
        date_str = date.strftime('%Y%m%d')

        # Only show progress bar in debug mode.
        iter_range = range(10000)
        if debug:
            iter_range = tqdm(iter_range)

        for i in iter_range:
            # No more news to crawl.
            if fail_count >= CONTINUE_FAIL_COUNT:
                break

            url = f'https://www.cna.com.tw/news/aipl/{date_str}{i:04d}.aspx'
            response = requests.get(url)

            # Got banned.
            if response.status_code == 403:
                logger.update(['Got banned.'])
                news.crawlers.util.after_banned_sleep()
                fail_count += 1
                continue

            # Missing news or no news.
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
                parsed_news = news.preprocess.cna.parse(ori_news=News(
                    raw_xml=response.text,
                    url=url,
                ))
            except Exception as err:
                # Skip parsing if error.
                if err.args:
                    logger.update([err.args[0]])
                continue

            news_datetime = dateutil.parser.isoparse(parsed_news.datetime)
            if past_datetime > news_datetime or \
                    news_datetime > current_datetime:
                logger.update(['Time constraint violated.'])
                continue

            news_list.append(parsed_news)

            # Sleep to avoid banned.
            news.crawlers.util.before_banned_sleep()

        # Go back 1 day.
        date = date - timedelta(days=1)

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
    # Get database connection.
    conn = news.db.util.get_conn(db_name=db_name)
    cur = conn.cursor()
    news.db.create.create_table(cur=cur)

    news.db.write.write_new_records(
        cur=cur,
        news_list=get_news_list(
            current_datetime=current_datetime,
            debug=debug,
            past_datetime=past_datetime,
        ),
    )

    conn.commit()

    # Close database connection.
    conn.close()
