from collections import Counter
from typing import Dict, Final, List, Optional

from tqdm import tqdm

import news.crawlers.db.create
import news.crawlers.db.util
import news.crawlers.db.write
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.crawlers.util.status_code
import news.db
from news.crawlers.db.schema import RawNews

FIRST_PAGE = 1
MAX_PAGE = 26
COMPANY_ID = news.crawlers.util.normalize.get_company_id(company='自由')


def get_news_list(
    category: str,
    api: str,
    *,
    debug: Optional[bool] = False,
    **kwargs: Optional[Dict],
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
            response = news.crawlers.util.request_url(url=page_url)

            # Raise exception if status code is not 200.
            news.crawlers.util.status_code.check_status_code(
                company_id=COMPANY_ID,
                status_code=response.status_code,
                url=page_url,
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
                response = news.crawlers.util.request_url(url=news_url)

                # Raise exception if status code is not 200.
                news.crawlers.util.status_code.check_status_code(
                    company_id=COMPANY_ID,
                    status_code=response.status_code,
                    url=news_url,
                )

                news_list.append(RawNews(
                    company_id=COMPANY_ID,
                    raw_xml=news.crawlers.util.normalize.compress_raw_xml(
                        raw_xml=response.text),
                    url_pattern=news.crawlers.util.normalize.compress_url(
                        url=news_url, company_id=COMPANY_ID),
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
    debug: Optional[bool] = False,
    **kwargs: Optional[Dict],
):

    # Get database connection.
    db_path = news.crawlers.db.util.get_db_path(db_name=db_name)
    conn = news.db.get_conn(db_path=db_path)
    cur = conn.cursor()

    # Ensure news table exists.
    news.crawlers.db.create.create_table(cur=cur)

    for category, api in CATEGORIES.items():
        # Get news list.
        news_list = get_news_list(
            api=api,
            category=category,
            debug=debug,
        )

        # Write news records to database.
        news.crawlers.db.write.write_new_records(cur=cur, news_list=news_list)
        conn.commit()

    # Close database connection.
    conn.close()
