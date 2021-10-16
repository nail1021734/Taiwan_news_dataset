from collections import Counter
from datetime import datetime, timedelta, timezone
from typing import Dict, Final, List, Optional

from tqdm import trange

import news.crawlers.db.create
import news.crawlers.db.util
import news.crawlers.db.write
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.crawlers.util.status_code
import news.db
from news.crawlers.db.schema import RawNews

COMPANY_ID: Final[int] = news.crawlers.util.normalize.get_company_id(
    company='中央社',
)
COMPANY_URL: Final[str] = news.crawlers.util.normalize.get_company_url(
    company_id=COMPANY_ID,
)


def get_news_list(
    current_datetime: Final[datetime],
    *,
    continue_fail_count: Final[Optional[int]] = 100,
    debug: Final[Optional[bool]] = False,
    max_news_per_day: Final[Optional[int]] = 10000,
    **kwargs: Final[Optional[Dict]],
) -> List[RawNews]:
    news_list: List[RawNews] = []
    logger = Counter()
    fail_count = 0
    datetime_str = current_datetime.strftime('%Y%m%d')

    # Only show progress bar in debug mode.
    for news_idx in trange(
            max_news_per_day,
            desc='Crawling',
            disable=not debug,
            dynamic_ncols=True,
    ):
        url = f'{COMPANY_URL}{datetime_str}{news_idx:04d}.aspx'
        try:
            response = news.crawlers.util.request_url.get(url=url)

            # Raise exception if status code is not 200.
            news.crawlers.util.status_code.check_status_code(
                company_id=COMPANY_ID,
                status_code=response.status_code,
                url=url,
            )

            news_list.append(
                RawNews(
                    company_id=COMPANY_ID,
                    raw_xml=news.crawlers.util.normalize.compress_raw_xml(
                        raw_xml=response.text,
                    ),
                    url_pattern=news.crawlers.util.normalize.compress_url(
                        url=url,
                        company_id=COMPANY_ID,
                    ),
                )
            )

            # Reset `fail_count` if no error occurred.
            fail_count = 0
        except Exception as err:
            fail_count += 1

            if err.args:
                logger.update([err.args[0]])

        # No more news to crawl.
        if fail_count >= continue_fail_count:
            break

    # Only show error statistics in debug mode.
    if debug:
        for k, v in logger.items():
            print(f'{k}: {v}')

    return news_list


def main(
    current_datetime: Final[datetime],
    db_name: Final[str],
    past_datetime: Final[datetime],
    **kwargs: Final[Optional[Dict]],
) -> None:
    # Value check.
    if current_datetime.tzinfo != timezone.utc:
        raise ValueError('`current_datetime` must in utc timezone.')
    if past_datetime.tzinfo != timezone.utc:
        raise ValueError('`past_datetime` must in utc timezone.')
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
        news_list = get_news_list(current_datetime=loop_datetime, **kwargs)

        # Write news records to database.
        news.crawlers.db.write.write_new_records(cur=cur, news_list=news_list)
        conn.commit()

        # Go back 1 day.
        loop_datetime = loop_datetime - timedelta(days=1)

    # Close database connection.
    conn.close()
