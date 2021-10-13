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
COMPANY_ID = news.crawlers.util.normalize.get_company_id(company='民視')

CATEGORIES = {
    'A': '體育',
    'C': '一般',
    'F': '財經',
    'I': '國際',
    'J': '美食',
    'L': '生活',
    'N': '社會',
    'P': '政治',
    'R': '美食',
    'S': '社會',
    'U': '社會',
    'W': '一般',
}


def get_news_list(
    category: str,
    current_datetime: datetime,
    api: str,
    past_datetime: datetime,
    *,
    debug: Final[Optional[bool]] = False,
    **kwargs: Final[Optional[Dict]],
) -> List[RawNews]:
    news_list: List[RawNews] = []
    logger = Counter()

    date = current_datetime

    fail_count = 0
    date_str = \
        f'{date.strftime("%Y")}{int(date.strftime("%m")):x}{date.strftime("%d")}'

    # W類別的新聞index比較長
    if api == 'W':
        iter_range = range(10000)
    else:
        iter_range = range(30)

    # Only show progress bar in debug mode.
    if debug:
        iter_range = tqdm(iter_range)

    for i in iter_range:
        # No more news to crawl.
        if fail_count >= CONTINUE_FAIL_COUNT:
            break

        if api == 'W':
            url = f'https://www.ftvnews.com.tw/news/detail/{date_str}{api}{i:04}'
        else:
            url = f'https://www.ftvnews.com.tw/news/detail/{date_str}{api}{i:02}M1'

        try:
            response = news.crawlers.util.request_url.get(url=url)

            # Raise exception if status code is not 200.
            news.crawlers.util.status_code.check_status_code(
                company_id=COMPANY_ID,
                status_code=response.status_code,
                url=url,
            )
            # Check if page exist.
            if not news.crawlers.util.pre_parse.check_ftv_page_exist(url):
                continue

            # If `status_code == 200` and successfully parsed (only happend when
            # such news is not missing), reset `fail_count`.
            fail_count = 0

            news_list.append(
                RawNews(
                    company_id=COMPANY_ID,
                    raw_xml=news.crawlers.util.normalize.compress_raw_xml(
                        raw_xml=response.text
                    ),
                    url_pattern=news.crawlers.util.normalize.compress_url(
                        url=url, company_id=COMPANY_ID
                    ),
                )
            )
        except Exception as err:
            fail_count += 1

            if err.args:
                logger.update([err.args[0]])
            continue

    # Only show error statistics in debug mode.
    if debug:
        for k, v in logger.items():
            print(f'{k}: {v}')

    return news_list


def main(
    current_datetime: datetime,
    db_name: str,
    past_datetime: datetime,
    **kwargs: Final[Optional[Dict]],
) -> None:
    # Value check.
    if past_datetime > current_datetime:
        raise ValueError('Must have `past_datetime <= current_datetime`.')

    # Get database connection.
    db_path = news.crawlers.db.util.get_db_path(db_name=db_name)
    conn = news.db.get_conn(db_path=db_path)
    cur = conn.cursor()

    # Ensure news table exists.
    news.crawlers.db.create.create_table(cur=cur)

    for api, category in CATEGORIES.items():
        date = current_datetime
        # Commit database once a day.
        while date >= past_datetime:
            # Get news list.
            news_list = get_news_list(
                category=category,
                current_datetime=date,
                api=api,
                past_datetime=date - timedelta(days=1),
                **kwargs,
            )

            # Write news records to database.
            news.crawlers.db.write.write_new_records(
                cur=cur,
                news_list=news_list,
            )
            conn.commit()

            # Go back 1 day.
            date = date - timedelta(days=1)

    # Close database connection.
    conn.close()
