from collections import Counter
from typing import List

import requests
from tqdm import tqdm

import news.crawlers
from news.crawlers.util.normalize import (
    company_id,
    compress_raw_xml,
    compress_url
)
from news.crawlers.db.schema import RawNews

FIRST_PAGE = 1
MAX_PAGE = 26
COMPANY = '自由'


def get_news_list(
    category: str,
    api: str,
    *,
    debug: bool = False,
) -> List[RawNews]:
    news_list: List[RawNews] = []
    logger = Counter()

    # Only show progress bar in debug mode.
    iter_range = range(FIRST_PAGE, MAX_PAGE)
    if debug:
        iter_range = tqdm(iter_range, desc='Crawling loop.')

    # Crawling loop.
    for page in iter_range:

        page_url = f'https://news.ltn.com.tw/ajax/breakingnews/{api}/{page}'

        try:
            response = requests.get(
                page_url,
                timeout=news.crawlers.util.status_code.REQUEST_TIMEOUT,
            )
            response.close()

            # Raise exception if status code is not 200.
            news.crawlers.util.status_code.check_status_code(
                company='ltn',
                response=response
            )

            # If `status_code == 200`, parse links in this page.
            api_json = response.json()['data']
            # Inconsistent api format.
            if page != 1:
                api_json = api_json.values()
        except Exception as err:
            if err.args:
                logger.update([err.args[0]])
            continue

        for news_dict in api_json:
            try:
                news_url = news_dict['url']
                response = requests.get(
                    news_url,
                    timeout=news.crawlers.util.status_code.REQUEST_TIMEOUT,
                )
                response.close()

                # Raise exception if status code is not 200.
                news.crawlers.util.status_code.check_status_code(
                    company='ltn',
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


CATEGORIES = {
    '政治': 'politics',
    '社會': 'society',
    '生活': 'life',
    '國際': 'world',
    '地方': 'local',
    '蒐奇': 'novelty',
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

    for category, api in CATEGORIES.items():
        news.crawlers.db.write.write_new_records(
            cur=cur,
            news_list=get_news_list(
                api=api,
                category=category,
                debug=debug,
            ),
        )

        conn.commit()

    # Close database connection.
    conn.close()
