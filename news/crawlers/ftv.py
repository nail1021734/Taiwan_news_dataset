from collections import Counter
from datetime import datetime, timedelta, timezone
from typing import Dict, Final, List, Optional

from bs4 import BeautifulSoup
from tqdm import trange

import news.crawlers.db.create
import news.crawlers.db.util
import news.crawlers.db.write
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.crawlers.util.status_code
import news.db
from news.crawlers.db.schema import RawNews

CATEGORY_API_LOOKUP_TABLE: Final[Dict[str, str]] = {
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
COMPANY_ID: Final[int] = news.crawlers.util.normalize.get_company_id(
    company='民視',
)
COMPANY_URL: Final[str] = news.crawlers.util.normalize.get_company_url(
    company_id=COMPANY_ID,
)


def page_not_found(raw_xml: Final[str]) -> bool:
    r"""Return `True` if page not found.

    This is need since FTV always return 200.
    """
    soup = BeautifulSoup(raw_xml, 'html.parser')
    script_tags = soup.select('script')

    # 如果網頁不存在, 則第 0 個 script tag 內會有 alert 這個 function.
    return script_tags \
        and script_tags[0].string \
        and script_tags[0].string[:5] == 'alert'


def get_news_list(
    category_api: Final[str],
    current_datetime: Final[datetime],
    *,
    continue_fail_count: Final[Optional[int]] = 100,
    debug: Final[Optional[bool]] = False,
    **kwargs: Final[Optional[Dict]],
) -> List[RawNews]:
    news_list: List[RawNews] = []
    logger = Counter()
    fail_count = 0

    # Month is hexidecimal.
    datetime_str = ''.join(
        [
            current_datetime.strftime('%Y'),
            hex(current_datetime.month)[-1].upper(),
            current_datetime.strftime('%d'),
        ]
    )

    # W 類別的新聞 index 範圍比較大.
    if category_api == 'W':
        max_news_per_day = 10000
    else:
        max_news_per_day = 30

    # `news_idx` start with 1.  Only show progress bar in debug mode.
    for news_idx in trange(
            1,
            max_news_per_day,
            desc='Crawling',
            disable=not debug,
            dynamic_ncols=True,
    ):
        if category_api == 'W':
            url = f'{COMPANY_URL}{datetime_str}{category_api}{news_idx:04}'
        else:
            url = f'{COMPANY_URL}{datetime_str}{category_api}{news_idx:02}M1'

        try:
            response = news.crawlers.util.request_url.get(url=url)

            # Raise exception if status code is not 200.
            news.crawlers.util.status_code.check_status_code(
                company_id=COMPANY_ID,
                status_code=response.status_code,
                url=url,
            )

            # Skip if page does not exist.
            if page_not_found(raw_xml=response.text):
                raise Exception('URL not found.')

            news_list.append(
                RawNews(
                    company_id=COMPANY_ID,
                    raw_xml=news.crawlers.util.normalize.compress_raw_xml(
                        raw_xml=response.text
                    ),
                    url_pattern=news.crawlers.util.normalize.compress_url(
                        url=url,
                        company_id=COMPANY_ID,
                    ),
                )
            )

            # Reset `fail_count` when `status_code == 200` and page is found.
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

    for category_api in CATEGORY_API_LOOKUP_TABLE.keys():
        # Commit database once a day.
        loop_datetime = current_datetime
        while loop_datetime >= past_datetime:
            # Get news list.
            news_list = get_news_list(
                category_api=category_api,
                current_datetime=loop_datetime,
                **kwargs,
            )

            # Write news records to database.
            news.crawlers.db.write.write_new_records(
                cur=cur,
                news_list=news_list,
            )
            conn.commit()

            # Go back 1 day.
            loop_datetime = loop_datetime - timedelta(days=1)

    # Close database connection.
    conn.close()
