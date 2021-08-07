from collections import Counter
from typing import List

import requests
from tqdm import tqdm

import news.crawlers
from news.crawlers.db.schema import RawNews
from news.crawlers.util.normalize import (company_id, compress_raw_xml,
                                          compress_url)

RECORD_PER_COMMIT = 1000
COMPANY = '三立'


def get_news_list(
    api: int,
    *,
    debug: bool = True,
) -> List[RawNews]:
    news_list: List[RawNews] = []
    logger = Counter()

    # Setn only 20 page per category.
    iter_range = range(1, 21)

    # Only show progress bar in debug mode.
    if debug:
        iter_range = tqdm(iter_range)

    for page in iter_range:
        url = f'https://www.setn.com/ViewAll.aspx?PageGroupID={api}&p={page}'

        try:
            news_url_patterns = news.crawlers.util.pre_parse.get_setn_link(url)
            for news_url_pattern in news_url_patterns:
                news_url = 'https://www.setn.com' + news_url_pattern

                response = requests.get(
                    news_url,
                    timeout=news.crawlers.util.status_code.REQUEST_TIMEOUT,
                )
                response.close()

                # Raise exception if status code is not 200.
                news.crawlers.util.status_code.check_status_code(
                    company='setn',
                    response=response
                )

                news_list.append(RawNews(
                    company_id=company_id(COMPANY),
                    raw_xml=compress_raw_xml(response.text),
                    url_pattern=compress_url(news_url),
                ))
        except Exception as err:
            if err.args:
                logger.update([err.args[0]])

    # Only show error stats in debug mode.
    if debug:
        for k, v in logger.items():
            print(f'{k}: {v}')

    return news_list


CATEGORY = {
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
    '寵物': 47,
}


def main(
    db_name: str,
    *,
    debug: bool = False,
):
    # Get database connection.
    conn = news.crawlers.db.util.get_conn(db_name=f'{db_name}')
    cur = conn.cursor()
    news.crawlers.db.create.create_table(cur=cur)

    for category, api in CATEGORY.items():
        news_list = get_news_list(
            debug=debug,
            api=api
        )

        if not news_list:
            # No more news to crawl.
            break

        news.crawlers.db.write.write_new_records(cur=cur, news_list=news_list)

        conn.commit()
    # Close database connection.
    conn.close()
