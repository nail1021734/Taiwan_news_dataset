from collections import Counter
from typing import Dict, List, Optional

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

COMPANY_ID: int = news.crawlers.util.normalize.get_company_id(company='風傳媒',)
COMPANY_URL: str = news.crawlers.util.normalize.get_company_url(
    company_id=COMPANY_ID,
)


def page_not_found(raw_xml: str) -> bool:
    r"""Return `True` if page not found.

    This is need since storm.mg always return 200.
    """
    soup = BeautifulSoup(raw_xml, 'html.parser')

    # 若網頁不存在則沒有 id 為 article_title 的 h1 tag.
    return not bool(soup.select('h1#article_title'))


def get_news_list(
    first_idx: int,
    latest_idx: int,
    *,
    continue_fail_count: Optional[int] = 500,
    debug: Optional[bool] = False,
    **kwargs: Optional[Dict],
) -> List[RawNews]:
    news_list: List[RawNews] = []
    logger = Counter()
    fail_count = 0

    # Only show progress bar in debug mode.
    for news_idx in trange(
            first_idx,
            latest_idx,
            desc='Crawling',
            disable=not debug,
            dynamic_ncols=True,
    ):
        # 多頁新聞可以用 `mode=whole` 得到全文.
        url = f'{COMPANY_URL}{news_idx}?mode=whole'
        try:
            response = news.crawlers.util.request_url.get(url=url)

            # Raise exception if status code is not 200.
            news.crawlers.util.status_code.check_status_code(
                company_id=COMPANY_ID,
                status_code=response.status_code,
                url=url,
            )

            if page_not_found(raw_xml=response.text):
                raise Exception('URL not found.')

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
    db_name: str,
    first_idx: int,
    latest_idx: int,
    *,
    records_per_commit: Optional[int] = 2000,
    **kwargs: Optional[Dict],
) -> None:
    # Value check.
    if first_idx <= 0:
        raise ValueError('Must have `first_idx > 0`.')

    # `latest_id` 為 -1 表示抓到沒有新聞為止.
    if latest_idx != -1:
        if latest_idx <= 0:
            raise ValueError(
                'Must have `latest_idx > 0` or `latest_idx == -1`.'
            )
        if first_idx > latest_idx:
            raise ValueError(
                'Must have `first_idx <= latest_idx` or `latest_idx == -1`.'
            )

    # Get database connection.
    db_path = news.crawlers.db.util.get_db_path(db_name=db_name)
    conn = news.db.get_conn(db_path=db_path)
    cur = conn.cursor()

    # Ensure news table exists.
    news.crawlers.db.create.create_table(cur=cur)

    cur_first_idx = first_idx
    while cur_first_idx <= latest_idx or latest_idx == -1:
        cur_latest_idx = cur_first_idx + records_per_commit

        # `cur_latest_idx` is bounded above by `latest_idx`. Use
        # `latest_idx + 1` to make range inclusive.
        if latest_idx != -1:
            cur_latest_idx = min(cur_latest_idx, latest_idx + 1)

        # Get news list.
        news_list = get_news_list(
            first_idx=cur_first_idx,
            latest_idx=cur_latest_idx,
            **kwargs,
        )

        # No more news to crawl.
        if not news_list and latest_idx == -1:
            break

        # Write news records to database.
        news.crawlers.db.write.write_new_records(cur=cur, news_list=news_list)
        conn.commit()

        # Increase crawling index.
        cur_first_idx += records_per_commit

    # Close database connection.
    conn.close()
