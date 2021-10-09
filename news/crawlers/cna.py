from collections import Counter
from datetime import datetime, timedelta
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

CONTINUE_FAIL_COUNT = 100
COMPANY_ID = news.crawlers.util.normalize.get_company_id(company='中央社')


def get_news_list(
    current_datetime: datetime,
    past_datetime: datetime,
    *,
    debug: Optional[bool] = False,
    **kwargs: Optional[Dict],
) -> List[RawNews]:
    news_list: List[RawNews] = []
    logger = Counter()

    date = current_datetime

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
        try:
            response = news.crawlers.util.request_url.get(url=url)

            # Raise exception if status code is not 200.
            news.crawlers.util.status_code.check_status_code(
                company_id=COMPANY_ID,
                status_code=response.status_code,
                url=url,
            )

            # If `status_code == 200`, reset `fail_count`.
            fail_count = 0

            news_list.append(RawNews(
                company_id=COMPANY_ID,
                raw_xml=news.crawlers.util.normalize.compress_raw_xml(
                    raw_xml=response.text),
                url_pattern=news.crawlers.util.normalize.compress_url(
                    url=url, company_id=COMPANY_ID),
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
    debug: Optional[bool] = False,
    **kwargs: Optional[Dict],
) -> None:
    if past_datetime > current_datetime:
        raise ValueError('Must have `past_datetime <= current_datetime`.')

    # Get database connection.
    db_path = news.crawlers.db.util.get_db_path(db_name=db_name)
    conn = news.db.get_conn(db_path=db_path)
    cur = conn.cursor()

    # Ensure news table exists.
    news.crawlers.db.create.create_table(cur=cur)

    # Commit transaction for each day.
    loop_datetime = current_datetime
    while loop_datetime >= past_datetime:
        # Get news list.
        news_list = get_news_list(
            current_datetime=loop_datetime,
            debug=debug,
            past_datetime=loop_datetime - timedelta(days=1),
        )

        # Write news records to database.
        news.crawlers.db.write.write_new_records(cur=cur, news_list=news_list)
        conn.commit()

        # Go back 1 day.
        loop_datetime = loop_datetime - timedelta(days=1)

    # Close database connection.
    conn.close()
