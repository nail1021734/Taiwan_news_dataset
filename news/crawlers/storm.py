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

RECORD_PER_COMMIT = 2000
COMPANY_ID = news.crawlers.util.normalize.get_company_id(company='風傳媒')


def get_news_list(
    first_idx: int,
    latest_idx: int,
    *,
    debug: Optional[bool] = False,
    **kwargs: Optional[Dict],
) -> List[RawNews]:
    news_list: List[RawNews] = []
    logger = Counter()

    iter_range = range(first_idx, latest_idx)
    # Only show progress bar in debug mode.
    if debug:
        iter_range = tqdm(iter_range)

    for idx in iter_range:
        url = f'https://www.storm.mg/article/{idx}'

        try:
            response = news.crawlers.util.request_url.get(url=url)

            # Raise exception if status code is not 200.
            news.crawlers.util.status_code.check_status_code(
                company_id=COMPANY_ID,
                status_code=response.status_code,
                url=url,
            )

            if not news.crawlers.util.pre_parse.check_storm_page_exist(url):
                continue
            news_list.append(RawNews(
                company_id=COMPANY_ID,
                raw_xml=news.crawlers.util.normalize.compress_raw_xml(
                    raw_xml=response.text),
                url_pattern=news.crawlers.util.normalize.compress_url(
                    url=url, company_id=COMPANY_ID),
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
    debug: Optional[bool] = False,
    **kwargs: Optional[Dict],
):
    if first_idx > latest_idx and latest_idx != -1:
        raise ValueError(
            'Must have `first_idx <= latest_idx` or `latest_idx == -1`'
        )

    # Get database connection.
    db_path = news.crawlers.db.util.get_db_path(db_name=db_name)
    conn = news.db.get_conn(db_path=db_path)
    cur = conn.cursor()

    # Ensure news table exists.
    news.crawlers.db.create.create_table(cur=cur)

    while first_idx <= latest_idx or latest_idx == -1:
        cur_latest_idx = first_idx + RECORD_PER_COMMIT
        if latest_idx != -1:
            cur_latest_idx = min(cur_latest_idx, latest_idx)

            # Make range inclusive.
            if cur_latest_idx == latest_idx:
                cur_latest_idx += 1

        # Get news list.
        news_list = get_news_list(
            debug=debug,
            first_idx=first_idx,
            latest_idx=cur_latest_idx,
        )

        # No more news to crawl.
        if not news_list:
            break

        # Write news records to database.
        news.crawlers.db.write.write_new_records(cur=cur, news_list=news_list)
        conn.commit()

        first_idx += RECORD_PER_COMMIT

    # Close database connection.
    conn.close()
