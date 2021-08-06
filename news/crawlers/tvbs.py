import re
from collections import Counter
from typing import List

import requests
from tqdm import tqdm

import news.crawlers
from news.crawlers.db.schema import RawNews
from news.crawlers.util.normalize import (company_id, compress_raw_xml,
                                          compress_url)

RECORD_PER_COMMIT = 1000
CATEGORIES = {
    'local': 1,
    'life': 2,
    'world': 3,
    'entertainment': 5,
    'china': 6,
    'politics': 7,
    'sports': 8,
    'tech': 12,
    'focus': 41,
    'fun': 50,
    'travel': 260,
    'health': 262,
    'cars': 269,
    'money': 270,
}
COMPANY = 'tvbs'


def get_news_list(
    category: str,
    category_id: int,
    first_idx: int,
    latest_idx: int,
    *,
    debug: bool = True,
) -> List[RawNews]:
    news_list: List[RawNews] = []
    logger = Counter()

    # Only show progress bar in debug mode.
    iter_range = range(latest_idx, first_idx, -1)
    if debug:
        iter_range = tqdm(iter_range, desc='Find latest idx loop.')

    data_obj = None
    # Find latest idx loop:
    for idx in iter_range:
        url = f'https://news.tvbs.com.tw/news/LoadMoreOverview?limit=100&offset=0&cateid={category_id}&cate={category}&newsid={idx}'
        try:
            response = requests.get(
                url,
                timeout=news.crawlers.util.status_code.REQUEST_TIMEOUT,
            )
            response.close()

            # Raise exception if status code is not 200.
            news.crawlers.util.status_code.check_status_code(
                company='tvbs',
                response=response
            )

            data_obj = response.json()

            # Successfully find the latest idx.
            if data_obj['newsid']:
                break
        except Exception as err:
            if err.args:
                logger.update([err.args[0]])

    # No news were found.
    if not data_obj or not data_obj['newsid'] or not data_obj['news_id_list']:
        return []

    # Get news id within specified range.
    news_idx_list = data_obj['news_id_list'].split(',')[1:]
    news_idx_list = map(
        lambda idx_str: int(idx_str[1:-1]),
        news_idx_list,
    )
    news_idx_list = filter(
        lambda idx: first_idx <= idx <= latest_idx,
        news_idx_list,
    )
    news_idx_list = list(news_idx_list)

    # Only show progress bar in debug mode.
    if debug:
        iter_range = tqdm(desc='Find ids loop.')

    # Loop to find the next first id.
    next_idx = int(data_obj['newsid'])
    data_obj = None
    while first_idx <= next_idx <= latest_idx:
        url = f'https://news.tvbs.com.tw/news/LoadMoreOverview?limit=100&offset=0&cateid={category_id}&cate={category}&newsid={next_idx}'

        try:
            response = requests.get(
                url,
                timeout=news.crawlers.util.status_code.REQUEST_TIMEOUT,
            )
            response.close()

            # Raise exception if status code is not 200.
            news.crawlers.util.status_code.check_status_code(
                company='tvbs',
                response=response
            )

            data_obj = response.json()

            # No mext first idx were found.
            if not data_obj or not data_obj['newsid'] or not data_obj['news_id_list']:
                break

            # Successfully find the next first idx and update next first id.
            next_idx = int(data_obj['newsid'])

            # Get news id within specified range.
            next_news_idx_list = filter(
                bool,
                data_obj['news_id_list'].split(','),
            )
            next_news_idx_list = map(
                lambda idx: re.search(r'(\d+)', idx).group(1),
                next_news_idx_list,
            )
            next_news_idx_list = map(int, next_news_idx_list)
            next_news_idx_list = filter(
                lambda idx: first_idx <= idx <= latest_idx,
                next_news_idx_list,
            )

            # Combine next news idx list into existed news idx list.
            news_idx_list.extend(list(next_news_idx_list))
        except Exception as err:
            if err.args:
                logger.update([err.args[0]])

        if debug:
            iter_range.update()

    # Crawling loop.
    news_idx_list = list(set(news_idx_list))

    # Only show progress bar in debug mode.
    if debug:
        news_idx_list = tqdm(news_idx_list, desc='Crawling loop.')

    for idx in news_idx_list:
        url = f'https://news.tvbs.com.tw/{category}/{idx}'

        try:
            response = requests.get(
                url,
                timeout=news.crawlers.util.status_code.REQUEST_TIMEOUT,
            )
            response.close()

            # Raise exception if status code is not 200.
            news.crawlers.util.status_code.check_status_code(
                company='tvbs',
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
    if first_idx > latest_idx:
        raise ValueError('Must have `first_idx <= latest_idx`.')

    # Get database connection.
    conn = news.crawlers.db.util.get_conn(db_name=f'{db_name}')
    cur = conn.cursor()
    news.crawlers.db.create.create_table(cur=cur)

    while first_idx <= latest_idx:
        cur_first_idx = latest_idx - RECORD_PER_COMMIT
        cur_first_idx = max(cur_first_idx, first_idx)

        # Make range inclusive.
        if cur_first_idx == first_idx:
            cur_first_idx -= 1

        news_list = []

        for category, category_id in CATEGORIES.items():
            news_list.extend(get_news_list(
                category=category,
                category_id=category_id,
                debug=debug,
                first_idx=cur_first_idx,
                latest_idx=latest_idx,
            ))

        news.crawlers.db.write.write_new_records(cur=cur, news_list=news_list)

        conn.commit()

        latest_idx -= RECORD_PER_COMMIT

    # Close database connection.
    conn.close()
