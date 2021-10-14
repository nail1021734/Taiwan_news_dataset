import re
from collections import Counter
from datetime import datetime, timezone
from typing import Dict, Final, List, Optional, Union

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
    '國際': '202',
    '港澳': '205',
    '財經': '208',
    '健康': '1255',
    '體育': '211',
    '美國': '203',
    '大陸': '204',
    '文史': '647',
}
# Commit database when crawling 10 pages.
COMMIT_PAGE_INTERVAL: Final[int] = 10
COMPANY_ID: Final[int] = news.crawlers.util.normalize.get_company_id(
    company='新唐人',
)
COMPANY_URL: Final[str] = news.crawlers.util.normalize.get_company_url(
    company_id=COMPANY_ID,
)
DATE_PATTERN: Final[re.Pattern] = re.compile(
    COMPANY_URL + r'(\d+)/(\d+)/(\d+)/a\d+\.html',
)


def get_datetime_from_url(url: Final[str]) -> Union[datetime, None]:
    r"""從網址取得 ntdtv 新聞的日期."""
    match = DATE_PATTERN.match(url)

    if not match:
        return None

    return datetime(
        year=int(match.group(1)),
        month=int(match.group(2)),
        day=int(match.group(3)),
        tzinfo=timezone.utc,
    )


def get_max_page(
    category_api: Final[str],
    **kwargs: Final[Optional[Dict]],
) -> int:
    r"""Get total number of pages under specified category."""
    try:
        page_url = f'{COMPANY_URL}prog{category_api}/1'
        response = news.crawlers.util.request_url.get(url=page_url)

        # Raise exception if status code is not 200.
        news.crawlers.util.status_code.check_status_code(
            company_id=COMPANY_ID,
            status_code=response.status_code,
            url=page_url,
        )

        # Total page numbers can be found in the tags `a.page-numbers`.
        soup = BeautifulSoup(response.text, 'html.parser')
        max_page = soup.select('a.page-numbers')[-2].text
        # Numbers are comma separated.
        return int(max_page.replace(',', ''))
    except Exception:
        # Only 1 page is available.  This situation is unlikely to happen.
        # It's here to prevent any weird errors happened from codes above.
        return 1


def get_start_page(
    category_api: Final[str],
    current_datetime: Final[datetime],
    max_page: Final[int],
    past_datetime: Final[datetime],
    *,
    continue_fail_count: Final[Optional[int]] = 5,
    debug: Final[Optional[bool]] = False,
    first_page: Final[Optional[int]] = 1,
    **kwargs: Final[Optional[Dict]],
) -> int:
    r"""Get first page under specified category satisfying datetime constraint.

    Datetime constraint is the smallest page number contains the first news `n`
    satisfied `past_datetime <= n.datetime <= current_datetime`.

    `continue_fail_count` is set to small number since it is unlikely to fail.
    """
    logger = Counter()
    fail_count = 0

    # Only show progress bar in debug mode.  Use `max_page + 1` to make range
    # inclusive.
    for start_page in trange(
            first_page,
            max_page + 1,
            desc='Find start page',
            disable=not debug,
            dynamic_ncols=True,
    ):
        page_url = f'{COMPANY_URL}prog{category_api}/{start_page}'

        try:
            response = news.crawlers.util.request_url.get(url=page_url)

            # Raise exception if status code is not 200.
            news.crawlers.util.status_code.check_status_code(
                company_id=COMPANY_ID,
                status_code=response.status_code,
                url=page_url,
            )

            # Parse date in this page.
            soup = BeautifulSoup(response.text, 'html.parser')
            a_tags = soup.select(
                'div.post_list > div.list_wrapper > div.one_post div.title > a'
            )
            news_urls = map(lambda a_tag: a_tag['href'], a_tags)

            # 過濾掉找不到日期的網址.
            news_datetimes = filter(
                bool,
                map(get_datetime_from_url, news_urls),
            )

            news_datetimes = list(news_datetimes)

            # Reset fail counter.  Nothing happen means no failure occur.
            fail_count = 0

            # If dates of all news in the current page is newer than
            # `current_datetime`, then we keep searching.
            if min(news_datetimes) > current_datetime:
                continue

            # If dates of all news in the current page is older than
            # `past_datetime`, then is very likely the follow up pages does
            # not have any newer news.  And we simply stop searching.  This
            # statement is needed since for some datetime ranges there is no
            # news.
            if max(news_datetimes) < past_datetime:
                break

            # If dates of some news in the current page is within valid range,
            # then we found the smallest page to start crawling.
            if any(map(
                    lambda n: past_datetime <= n <= current_datetime,
                    news_datetimes,
            )):
                break
        except Exception as err:
            # Some pages may not be available.
            fail_count += 1

            if err.args:
                logger.update([err.args[0]])

        # This statement is here to prevent script from stop execution.
        if fail_count >= continue_fail_count:
            break

    # Only show error statistics in debug mode.
    if debug:
        for k, v in logger.items():
            print(f'{k}: {v}')

    return start_page


def get_news_list(
    category_api: Final[str],
    current_datetime: Final[datetime],
    first_page: Final[int],
    last_page: Final[int],
    past_datetime: Final[datetime],
    *,
    continue_fail_count: Final[Optional[int]] = 5,
    debug: Final[Optional[bool]] = False,
    **kwargs: Final[Optional[Dict]],
) -> List[RawNews]:
    news_list: List[RawNews] = []
    logger = Counter()
    fail_count = 0

    # Only show progress bar in debug mode.
    for page in trange(
            first_page,
            last_page,
            desc='Crawling',
            disable=not debug,
            dynamic_ncols=True,
    ):
        # Cannot get news.  This situation is highly likely due to bugs.
        if fail_count >= continue_fail_count:
            break

        # 抓取頁面內所有新聞的網址
        page_url = f'{COMPANY_URL}prog{category_api}/{page}'
        try:
            response = news.crawlers.util.request_url.get(url=page_url)

            # Raise exception if status code is not 200.
            news.crawlers.util.status_code.check_status_code(
                company_id=COMPANY_ID,
                status_code=response.status_code,
                url=page_url,
            )

            # Reset `fail_count` if no error occurred.
            fail_count = 0

            # Parse links in this page.
            soup = BeautifulSoup(response.text, 'html.parser')
            a_tags = soup.select(
                'div.post_list > div.list_wrapper > div.one_post div.title > a'
            )
            news_urls = map(lambda a_tag: a_tag['href'], a_tags)
        # Skip current page if any error occurred.
        except Exception as err:
            fail_count += 1

            if err.args:
                logger.update([f'In page {page}: {err.args[0]}'])
            continue

        # 抓取新聞原始碼
        for news_url in news_urls:
            try:
                news_datetime = get_datetime_from_url(url=news_url)

                # Skip if `news_datetime` is not in valid range.
                if not (past_datetime <= news_datetime <= current_datetime):
                    continue

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
                            raw_xml=response.text,
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

    for category_api in CATEGORY_API_LOOKUP_TABLE.values():
        # Get total number of pages.
        max_page = get_max_page(category_api=category_api, **kwargs)

        # Get starting page.
        start_page = get_start_page(
            category_api=category_api,
            current_datetime=current_datetime,
            max_page=max_page,
            past_datetime=past_datetime,
            **kwargs,
        )

        # Commit news list to database when crawling enough pages. Use
        # `max_page + 1` to make range inclusive.
        for page in range(
                start_page,
                max_page + 1,
                COMMIT_PAGE_INTERVAL,
        ):
            # Get news list.
            news_list = get_news_list(
                category_api=category_api,
                current_datetime=current_datetime,
                first_page=page,
                last_page=min(page + COMMIT_PAGE_INTERVAL, max_page),
                past_datetime=past_datetime,
                **kwargs,
            )

            # Stop crawling when `news_list` is empty.  This happens when news
            # violate `past_datetime` constraint.
            if not news_list:
                break

            # Write news records to database.
            news.crawlers.db.write.write_new_records(
                cur=cur,
                news_list=news_list,
            )
            conn.commit()

    # Close database connection.
    conn.close()
