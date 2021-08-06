from collections import Counter
from typing import List

import requests
from tqdm import tqdm

import news.crawlers
from news.crawlers.db.schema import RawNews
from news.crawlers.util.normalize import (company_id, compress_raw_xml,
                                          compress_url)

RECORD_PER_COMMIT = 1000
COMPANY = '東森'


def get_news_list(
    first_idx: int,
    latest_idx: int,
    *,
    debug: bool = True,
) -> List[RawNews]:
    news_list: List[RawNews] = []
    logger = Counter()

    iter_range = range(first_idx, latest_idx + 1)
    if debug:
        iter_range = tqdm(iter_range)

    for idx in iter_range:
        url = f'https://star.ettoday.net/news/{idx}'

        try:
            response = requests.get(
                url,
                timeout=news.crawlers.util.status_code.REQUEST_TIMEOUT,
            )
            response.close()

            # Raise exception if status code is not 200.
            news.crawlers.util.status_code.check_status_code(
                company='ettoday',
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

    # Only show error stats in debug mode.
    if debug:
        for k, v in logger.items():
            print(f'{k}: {v}')

    return news_list


def main(
    db_name: str,
    first_idx: int,
    latest_idx: int,
    *,
    debug: bool = False,
):
    if first_idx > latest_idx and latest_idx != -1:
        raise ValueError(
            'Must have `first_idx <= latest_idx` or `latest_idx == -1`'
        )

    # Get database connection.
    conn = news.crawlers.db.util.get_conn(db_name=f'{db_name}')
    cur = conn.cursor()
    news.crawlers.db.create.create_table(cur=cur)

    while first_idx <= latest_idx or latest_idx == -1:
        cur_latest_idx = first_idx + RECORD_PER_COMMIT
        if latest_idx != -1:
            cur_latest_idx = min(cur_latest_idx, latest_idx)

        news_list = get_news_list(
            debug=debug,
            first_idx=first_idx,
            latest_idx=cur_latest_idx,
        )

        if not news_list:
            # No more news to crawl.
            break

        news.crawlers.db.write.write_new_records(cur=cur, news_list=news_list)

        conn.commit()

        first_idx += RECORD_PER_COMMIT

    # Close database connection.
    conn.close()
