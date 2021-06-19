from collections import Counter
from typing import List

import requests
from tqdm import tqdm

import news.crawlers
from news.db.schema import News

RECORD_PER_COMMIT = 1000


def get_news_list(
    first_idx: int,
    latest_idx: int,
    *,
    debug: bool = True,
) -> List[News]:
    news_list: List[News] = []
    logger = Counter()

    iter_range = range(first_idx, latest_idx)
    if debug:
        iter_range = tqdm(iter_range)

    for idx in iter_range:
        url = f'https://www.setn.com/News.aspx?NewsID={idx}'

        try:
            response = requests.get(
                url,
                timeout=news.crawlers.util.REQUEST_TIMEOUT,
            )
            response.close()

            # Raise exception if status code is not 200.
            news.crawlers.util.check_status_code(
                company='setn',
                response=response
            )

            parsed_news = news.preprocess.setn.parse(ori_news=News(
                raw_xml=response.text,
                url=url,
            ))

            news_list.append(parsed_news)
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
    conn = news.db.util.get_conn(db_name=db_name)
    cur = conn.cursor()
    news.db.create.create_table(cur=cur)

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

        news.db.write.write_new_records(cur=cur, news_list=news_list)

        conn.commit()

        first_idx += RECORD_PER_COMMIT

    # Close database connection.
    conn.close()
