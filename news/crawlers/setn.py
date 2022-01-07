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

CATEGORY_API_LOOKUP_TABLE: Dict[str, str] = {
    '政治': '6',
    '社會': '41',
    '國際': '5',
    '生活': '4',
    '健康': '65',
    '運動': '34',
    '汽車': '12',
    '地方': '97',
    '名家': '9',
    '新奇': '42',
    '科技': '7',
    '財經': '2',
    '寵物': '47',
}
COMPANY_ID: int = news.crawlers.util.normalize.get_company_id(company='三立',)
COMPANY_URL: str = news.crawlers.util.normalize.get_company_url(
    company_id=COMPANY_ID,
)


def get_news_list(
    category_api: str,
    *,
    continue_fail_count: Optional[int] = 5,
    debug: Optional[bool] = False,
    first_page: Optional[int] = 1,
    max_page: Optional[int] = 20,
    **kwargs: Optional[Dict],
) -> List[RawNews]:
    news_list: List[RawNews] = []
    logger = Counter()
    fail_count = 0

    # Only show progress bar in debug mode.  Use `max_page + 1` to make range
    # inclusive.
    for page in trange(
            first_page,
            max_page + 1,
            desc='Crawling',
            disable=not debug,
            dynamic_ncols=True,
    ):
        # Cannot get news.  This situation is highly likely due to bugs.
        if fail_count >= continue_fail_count:
            break

        page_url = (
            f'{COMPANY_URL}ViewAll.aspx?PageGroupID={category_api}'
            + f'&p={page}'
        )

        try:
            # setn 新聞不是用 index 暴力爬, 需要先 parse 出每頁新聞的 url, 因此在這裡對
            # 每個 page 進行 parse, 回傳新聞網址.
            response = news.crawlers.util.request_url.get(url=page_url)

            # Raise exception if status code is not 200.
            news.crawlers.util.status_code.check_status_code(
                company_id=COMPANY_ID,
                status_code=response.status_code,
                url=page_url,
            )

            soup = BeautifulSoup(response.text, 'html.parser')

            a_tags = soup.select('div.newsItems h3.view-li-title > a')
            news_urls = map(lambda a_tag: a_tag['href'], a_tags)

            # Reset `fail_count` if no error occurred.
            fail_count = 0
        except Exception as err:
            fail_count += 1

            if err.args:
                logger.update([err.args[0]])
            continue

        for news_url in news_urls:
            try:
                # `news_url` start with '/', and `COMPANY_URL` end with '/'.
                news_url = f'{COMPANY_URL}{news_url[1:]}'
                response = news.crawlers.util.request_url.get(url=news_url)

                # Raise exception if status code is not 200.
                news.crawlers.util.status_code.check_status_code(
                    company_id=COMPANY_ID,
                    status_code=response.status_code,
                    url=news_url,
                )

                news_list.append(
                    RawNews(
                        company_id=COMPANY_ID,
                        raw_xml=news.crawlers.util.normalize.compress_raw_xml(
                            raw_xml=response.text
                        ),
                        url_pattern=news.crawlers.util.normalize.compress_url(
                            url=news_url,
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

            # Cannot get news.  This situation is highly likely due to bugs.
            if fail_count >= continue_fail_count:
                break

    # Only show error statistics in debug mode.
    if debug:
        for k, v in logger.items():
            print(f'{k}: {v}')

    return news_list


def main(
    db_name: str,
    **kwargs: Optional[Dict],
) -> None:
    # Get database connection.
    db_path = news.crawlers.db.util.get_db_path(db_name=db_name)
    conn = news.db.get_conn(db_path=db_path)
    cur = conn.cursor()

    # Ensure news table exists.
    news.crawlers.db.create.create_table(cur=cur)

    for category_api in CATEGORY_API_LOOKUP_TABLE.values():
        # Get news list.
        news_list = get_news_list(category_api=category_api, **kwargs)

        # No more news to crawl.
        if not news_list:
            break

        # Write news records to database.
        news.crawlers.db.write.write_new_records(cur=cur, news_list=news_list)
        conn.commit()

    # Close database connection.
    conn.close()
