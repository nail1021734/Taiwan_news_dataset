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

# Plus 1 to make range inclusive.
MAX_PAGE = 2672 + 1
PAGE_INTERVAL = 100
COMPANY = '聯合報'


def get_news_list(
    current_datetime: datetime,
    past_datetime: datetime,
    page_range: List[int],
    *,
    debug: bool = False,
) -> List[RawNews]:
    news_list: List[RawNews] = []
    logger = Counter()

    for channelId in [1, 2]:
        # Only show progress bar in debug mode.
        iter_range = range(page_range[0], page_range[1])
        if debug:
            iter_range = tqdm(iter_range)

        time_constraint_violated = False
        for page in iter_range:
            if time_constraint_violated:
                break

            url = f'https://udn.com/api/more?page={page}&channelId={channelId}&type=cate_latest_news&totalRecNo=100'
            try:
                response = requests.get(
                    url,
                    timeout=news.crawlers.util.status_code.REQUEST_TIMEOUT,
                )
                response.close()

                # Raise exception if status code is not 200.
                news.crawlers.util.status_code.check_status_code(
                    company='udn',
                    response=response
                )
            except Exception as err:
                if err.args:
                    logger.update([err.args[0]])
                break

            data_lists = response.json()
            if 'lists' not in data_lists or not data_lists['lists']:
                break

            for data_obj in data_lists['lists']:
                try:
                    news_datetime = datetime.strptime(
                        data_obj['time']['date'],
                        '%Y-%m-%d %H:%M'
                    ) - timedelta(hours=8)
                    news_datetime = dateutil.parser.isoparse(
                        news_datetime.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
                    )
                    if not (past_datetime <= news_datetime <= current_datetime):
                        raise Exception('Time constraint violated.')

                    url = data_obj["titleLink"].split("?")[0]
                    url = f'https://udn.com{url}'

                    response = requests.get(
                        url,
                        timeout=news.crawlers.util.status_code.REQUEST_TIMEOUT,
                    )
                    response.close()

                    # Raise exception if status code is not 200.
                    news.crawlers.util.status_code.check_status_code(
                        company='udn',
                        response=response
                    )

                    news_list.append(RawNews(
                        company_id=company_id(COMPANY),
                        raw_xml=compress_raw_xml(response.text),
                        url_pattern=compress_url(url),
                    ))
                except Exception as err:
                    if err.args:
                        logger.update([err.args[0]])

                        if err.args[0] == 'Time constraint violated.':
                            time_constraint_violated = True
                            break

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

    # Commit database when crawling 10 pages.
    for page in range(0, MAX_PAGE, PAGE_INTERVAL):
        page_range = [
            page,
            min(page + PAGE_INTERVAL, MAX_PAGE),
        ]
        news_list = get_news_list(
            current_datetime=current_datetime,
            debug=debug,
            page_range=page_range,
            past_datetime=past_datetime,
        )
        # When news violate `past_datetime` break for loop.
        if not news_list:
            break
        news.crawlers.db.write.write_new_records(
            cur=cur,
            news_list=news_list,
        )

        conn.commit()

    # Close database connection.
    conn.close()
